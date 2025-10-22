from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
import json
import os
import uuid
from datetime import datetime
import torch
import librosa
import numpy as np
from pathlib import Path
import shutil
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import phoneme service router
from phoneme_service import router as phoneme_router

# Import review API router
from review_api import router as review_router

# Import inference module
from inference import analyze_pronunciation as analyze_audio_phonemes
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
MODELS_DIR = BASE_DIR / "models"
MODEL_PATH = MODELS_DIR / "trained_model.pt"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)

# Load model (if available)
model = None
try:
    if MODEL_PATH.exists():
        model = torch.load(MODEL_PATH, map_location=torch.device('cpu'))
        model.eval()
        print("✓ Model loaded successfully")
    else:
        print("⚠ Model not found. Train the model first using the Colab notebook.")
except Exception as e:
    print(f"⚠ Could not load model: {e}")


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
        "model_loaded": model is not None
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
    
    # Save audio file
    audio_path = words_dir / f"{word_index:02d}_{word}.wav"
    with open(audio_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)
    
    # Analyze if model is available
    result = None
    if model is not None:
        try:
            result = await analyze_pronunciation(audio_path, word)
        except Exception as e:
            print(f"Analysis error: {e}")
            result = {
                "word": word,
                "score": 0.0,
                "confidence": 0.0,
                "feedback": "Model analysis unavailable"
            }
    else:
        result = {
            "word": word,
            "score": 0.0,
            "confidence": 0.0,
            "feedback": "Model not loaded. Please train the model first."
        }
    
    # Save analysis result
    result_path = words_dir / f"{word_index:02d}_{word}_result.json"
    with open(result_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    return result


async def analyze_pronunciation(audio_path: Path, word: str) -> dict:
    """Analyze pronunciation using the trained model."""
    try:
        # Load audio
        y, sr = librosa.load(audio_path, sr=16000)
        
        # Extract features (must match training pipeline)
        features = extract_features(y, sr)
        
        # Convert to tensor
        features_tensor = torch.FloatTensor(features).unsqueeze(0)
        
        # Inference
        with torch.no_grad():
            output = model(features_tensor)
            score = torch.sigmoid(output).item()
        
        # Generate feedback
        if score >= 0.8:
            feedback = "Mükemmel! Telaffuzunuz çok iyi."
        elif score >= 0.6:
            feedback = "İyi! Küçük iyileştirmeler yapabilirsiniz."
        elif score >= 0.4:
            feedback = "Orta düzey. Daha fazla pratik yapmalısınız."
        else:
            feedback = "Geliştirme gerekiyor. Telaffuzu tekrar deneyin."
        
        return {
            "word": word,
            "score": float(score),
            "confidence": 0.85,  # Placeholder
            "feedback": feedback
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


def extract_features(y: np.ndarray, sr: int) -> np.ndarray:
    """Extract acoustic features from audio signal."""
    # MFCCs
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfccs_mean = np.mean(mfccs, axis=1)
    mfccs_std = np.std(mfccs, axis=1)
    
    # Spectral features
    spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
    spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))
    zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(y))
    
    # RMS energy
    rms = np.mean(librosa.feature.rms(y=y))
    
    # Combine features
    features = np.concatenate([
        mfccs_mean,
        mfccs_std,
        [spectral_centroid, spectral_rolloff, zero_crossing_rate, rms]
    ])
    
    return features


@app.post("/analyze/audio")
async def analyze_audio_endpoint(
    file: UploadFile = File(...),
    word: str = Form(...)
):
    """
    Analyze pronunciation quality of uploaded audio file.
    Compares recorded audio with target phoneme sequence.
    
    Args:
        file: .wav audio file (UploadFile)
        word: Target word being pronounced
        
    Returns:
        JSON with phoneme analysis results
        
    Example:
        curl -X POST http://localhost:8000/analyze/audio \
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
        
        temp_file_path = temp_dir / f"{uuid.uuid4()}.wav"
        
        with open(temp_file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Generate target phonemes using phoneme service
        try:
            response = requests.post(
                "http://localhost:8000/phoneme/generate",
                json={"word": word, "include_stress": True}
            )
            
            if response.status_code == 200:
                phoneme_data = response.json()
                target_phonemes = phoneme_data['phonemes']
            else:
                # Fallback if phoneme service unavailable
                target_phonemes = ""
                
        except Exception as e:
            logger.warning(f"Phoneme service unavailable: {e}")
            target_phonemes = ""
        
        # Analyze pronunciation
        if target_phonemes:
            result = analyze_audio_phonemes(
                audio_path=str(temp_file_path),
                word=word,
                target_phonemes=target_phonemes
            )
        else:
            # Fallback to basic acoustic analysis only
            raise HTTPException(
                status_code=503,
                detail="Phoneme service unavailable. Cannot generate target phonemes."
            )
        
        # Clean up temporary file
        try:
            temp_file_path.unlink()
        except:
            pass
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Audio analysis failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Audio analysis failed: {str(e)}"
        )


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


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "data_dir": str(DATA_DIR),
        "participants": len(list(DATA_DIR.glob("participant_*")))
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
