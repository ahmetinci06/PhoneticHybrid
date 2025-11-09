from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
import json
import os
import uuid
from datetime import datetime
from pathlib import Path
import shutil
import logging
import librosa  # Still needed for audio format conversion
import soundfile as sf  # For saving WAV files

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import phoneme service router
from phoneme_service import router as phoneme_router

# Import review API router
from review_api import router as review_router

# Import inference module
from inference import analyze_pronunciation_whisper
import requests

app = FastAPI(title="Turkish Pronunciation Analysis API")

# CORS configuration for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include phoneme service router
app.include_router(phoneme_router)

# Include review API router
app.include_router(review_router)

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)

print("✓ PhoneticHybrid API - Using Whisper Speech Recognition")


# Pydantic models
class ParticipantInfo(BaseModel):
    name: str
    age: int
    gender: str
    consent: bool


class SurveyResponse(BaseModel):
    participant_id: str
    responses: List[int]  # Likert scale responses (1-5)


class AnalysisResult(BaseModel):
    word: str
    score: float
    confidence: float
    feedback: str


# Endpoints
@app.get("/")
async def root():
    return {
        "service": "Turkish Pronunciation Analysis",
        "status": "running",
        "analysis_method": "Whisper (OpenAI) + Phoneme Analysis"
    }


@app.post("/register")
async def register_participant(info: ParticipantInfo):
    """Register a new participant and create their data directory."""
    if not info.consent:
        raise HTTPException(status_code=400, detail="Consent is required")
    
    participant_id = str(uuid.uuid4())
    participant_dir = DATA_DIR / f"participant_{participant_id}"
    participant_dir.mkdir(exist_ok=True)
    
    # Save participant info
    info_path = participant_dir / "info.json"
    with open(info_path, "w", encoding="utf-8") as f:
        json.dump({
            "id": participant_id,
            "name": info.name,
            "age": info.age,
            "gender": info.gender,
            "consent": info.consent,
            "timestamp": datetime.now().isoformat()
        }, f, ensure_ascii=False, indent=2)
    
    return {"participant_id": participant_id, "status": "registered"}


@app.post("/survey")
async def save_survey(survey: SurveyResponse):
    """Save orthodontic literacy survey responses."""
    participant_dir = DATA_DIR / f"participant_{survey.participant_id}"
    
    if not participant_dir.exists():
        raise HTTPException(status_code=404, detail="Participant not found")
    
    survey_path = participant_dir / "survey.json"
    with open(survey_path, "w", encoding="utf-8") as f:
        json.dump({
            "participant_id": survey.participant_id,
            "responses": survey.responses,
            "timestamp": datetime.now().isoformat()
        }, f, ensure_ascii=False, indent=2)
    
    return {"status": "survey_saved"}


@app.post("/upload")
async def upload_audio(
    participant_id: str = Form(...),
    word: str = Form(...),
    word_index: int = Form(...),
    audio: UploadFile = File(...)
):
    """Upload and save pronunciation recording."""
    participant_dir = DATA_DIR / f"participant_{participant_id}"
    
    if not participant_dir.exists():
        raise HTTPException(status_code=404, detail="Participant not found")
    
    # Create words directory
    words_dir = participant_dir / "kelimeler"
    words_dir.mkdir(exist_ok=True)
    
    # Save temporary uploaded file
    temp_dir = Path("temp_audio")
    temp_dir.mkdir(exist_ok=True)
    temp_path = temp_dir / f"temp_{uuid.uuid4()}.webm"
    
    try:
        # Save uploaded file
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)
        
        # Convert to proper WAV format using librosa
        audio_path = words_dir / f"{word_index:02d}_{word}.wav"
        y, sr = librosa.load(str(temp_path), sr=16000)
        
        # Save as proper WAV file
        sf.write(str(audio_path), y, sr, subtype='PCM_16')
        
    finally:
        # Clean up temp file
        if temp_path.exists():
            temp_path.unlink()
    
    # This endpoint is deprecated - recordings are now analyzed via /analyze
    # This is kept for backward compatibility with older data collection
    result = {
        "word": word,
        "score": 0.0,
        "confidence": 0.0,
        "feedback": "Recording saved. Use /analyze endpoint for analysis."
    }
    
    # Save analysis result
    result_path = words_dir / f"{word_index:02d}_{word}_result.json"
    with open(result_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    return result


# Deprecated ML-based analysis functions removed
# Use /analyze endpoint for production analysis


@app.get("/audio/{participant_id}/{filename}")
async def serve_audio(participant_id: str, filename: str):
    """
    Serve audio files for review interface.
    
    Args:
        participant_id: Participant ID
        filename: Audio filename
    
    Returns:
        Audio file
    """
    audio_path = DATA_DIR / participant_id / "kelimeler" / filename
    
    if not audio_path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    return FileResponse(
        path=str(audio_path),
        media_type="audio/wav",
        filename=filename
    )


@app.post("/analyze")
async def analyze_endpoint(
    file: UploadFile = File(...),
    word: str = Form(...)
):
    """
    Analyze pronunciation using Whisper (OpenAI) + Phoneme Analysis.

    This production endpoint combines:
    - Whisper speech-to-text (local, open-source)
    - Phonemizer for ground-truth phoneme sequences
    - Acoustic feature analysis for detailed scoring

    Args:
        file: .wav audio file (UploadFile)
        word: Target word being pronounced

    Returns:
        JSON with comprehensive analysis results including:
        - recognized_text: What Whisper recognized
        - recognition_confidence: Whisper's confidence score
        - phonemes_target: Expected phoneme sequence
        - segment_scores: Per-phoneme pronunciation scores
        - overall: Combined overall score

    Example:
        curl -X POST http://localhost:8000/analyze \
          -F "file=@pencere.wav" \
          -F "word=pencere"
    """
    try:
        # Validate file format
        if not file.filename.endswith('.wav'):
            raise HTTPException(
                status_code=400,
                detail="Only .wav files are supported"
            )

        # Save uploaded file temporarily
        temp_dir = Path("temp_audio")
        temp_dir.mkdir(exist_ok=True)

        # Save raw upload first
        raw_temp_path = temp_dir / f"{uuid.uuid4()}_raw.wav"
        final_temp_path = temp_dir / f"{uuid.uuid4()}.wav"

        with open(raw_temp_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Convert to proper WAV format (16-bit PCM, 16kHz)
        # This ensures compatibility with Whisper, Praat, and librosa
        try:
            import soundfile as sf
            y, sr = librosa.load(str(raw_temp_path), sr=16000)
            sf.write(str(final_temp_path), y, 16000, subtype='PCM_16')
            logger.info(f"Audio converted to proper WAV format: {final_temp_path}")
        except Exception as e:
            logger.error(f"Audio conversion failed: {e}")
            # If conversion fails, try using the raw file
            final_temp_path = raw_temp_path

        # Analyze pronunciation using Whisper hybrid approach
        result = analyze_pronunciation_whisper(
            audio_path=str(final_temp_path),
            word=word
        )

        # Clean up temporary files
        try:
            if raw_temp_path.exists():
                raw_temp_path.unlink()
            if final_temp_path.exists() and final_temp_path != raw_temp_path:
                final_temp_path.unlink()
        except:
            pass

        return result

    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Server configuration error: {str(e)}"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Whisper analysis failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Audio analysis failed: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    # Check if Whisper is available
    whisper_available = False
    try:
        import whisper
        whisper_available = True
    except Exception:
        pass

    return {
        "status": "healthy",
        "whisper_available": whisper_available,
        "data_dir": str(DATA_DIR),
        "participants": len(list(DATA_DIR.glob("participant_*"))),
        "analysis_method": "Whisper (OpenAI) + Phoneme Analysis"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
