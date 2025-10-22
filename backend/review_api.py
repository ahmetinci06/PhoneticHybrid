"""
API endpoints for manual pronunciation review and labeling.
Used by human evaluators to score recordings for ML training.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from pathlib import Path
from datetime import datetime
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/review", tags=["review"])

DATA_DIR = Path("../data")


class LabelData(BaseModel):
    """Label/score data for a recording"""
    word: str
    score: float  # 0-100
    labeled: bool = True
    evaluator: str
    notes: Optional[str] = None
    timestamp: Optional[str] = None
    pronunciation_quality: Optional[str] = None  # excellent/good/fair/poor
    specific_issues: Optional[List[str]] = None  # ["pitch", "formants", "energy"]


class ParticipantSummary(BaseModel):
    """Summary of a participant"""
    participant_id: str
    total_recordings: int
    labeled_recordings: int
    unlabeled_recordings: int
    registration_date: Optional[str] = None
    survey_completed: bool


class RecordingInfo(BaseModel):
    """Information about a single recording"""
    filename: str
    word: str
    audio_path: str
    labeled: bool
    score: Optional[float] = None
    evaluator: Optional[str] = None
    notes: Optional[str] = None
    timestamp: Optional[str] = None


@router.get("/participants", response_model=List[ParticipantSummary])
async def list_participants():
    """
    Get list of all participants with summary information.
    
    Returns:
        List of participant summaries with recording counts
    """
    if not DATA_DIR.exists():
        return []
    
    participants = []
    
    for participant_dir in DATA_DIR.glob("participant_*"):
        participant_id = participant_dir.name
        
        # Count recordings
        kelimeler_dir = participant_dir / "kelimeler"
        total_recordings = 0
        labeled_recordings = 0
        
        if kelimeler_dir.exists():
            wav_files = list(kelimeler_dir.glob("*.wav"))
            total_recordings = len(wav_files)
            
            for wav_file in wav_files:
                result_file = wav_file.parent / f"{wav_file.stem}_result.json"
                if result_file.exists():
                    labeled_recordings += 1
        
        # Check for survey data
        survey_file = participant_dir / "survey.json"
        survey_completed = survey_file.exists()
        
        # Get registration info
        registration_file = participant_dir / "info.json"
        registration_date = None
        if registration_file.exists():
            try:
                with open(registration_file, 'r', encoding='utf-8') as f:
                    info = json.load(f)
                    registration_date = info.get('timestamp')
            except:
                pass
        
        participants.append(ParticipantSummary(
            participant_id=participant_id,
            total_recordings=total_recordings,
            labeled_recordings=labeled_recordings,
            unlabeled_recordings=total_recordings - labeled_recordings,
            registration_date=registration_date,
            survey_completed=survey_completed
        ))
    
    # Sort by most recent first
    participants.sort(key=lambda p: p.registration_date or "", reverse=True)
    
    return participants


@router.get("/participants/{participant_id}")
async def get_participant_details(participant_id: str):
    """
    Get detailed information about a specific participant.
    
    Args:
        participant_id: Participant ID (e.g., "participant_XXX")
    
    Returns:
        Participant details including recordings, survey data, and info
    """
    participant_dir = DATA_DIR / participant_id
    
    if not participant_dir.exists():
        raise HTTPException(status_code=404, detail="Participant not found")
    
    # Get participant info
    info_file = participant_dir / "info.json"
    participant_info = {}
    if info_file.exists():
        with open(info_file, 'r', encoding='utf-8') as f:
            participant_info = json.load(f)
    
    # Get survey data
    survey_file = participant_dir / "survey.json"
    survey_data = None
    if survey_file.exists():
        with open(survey_file, 'r', encoding='utf-8') as f:
            survey_data = json.load(f)
    
    # Get recordings
    kelimeler_dir = participant_dir / "kelimeler"
    recordings = []
    
    if kelimeler_dir.exists():
        for wav_file in sorted(kelimeler_dir.glob("*.wav")):
            result_file = wav_file.parent / f"{wav_file.stem}_result.json"
            
            labeled = result_file.exists()
            score = None
            evaluator = None
            notes = None
            timestamp = None
            
            if labeled:
                try:
                    with open(result_file, 'r', encoding='utf-8') as f:
                        result = json.load(f)
                        score = result.get('score')
                        evaluator = result.get('evaluator')
                        notes = result.get('notes')
                        timestamp = result.get('timestamp')
                except Exception as e:
                    logger.error(f"Error reading result file {result_file}: {e}")
            
            # Extract word from filename (e.g., "01_araba.wav" -> "araba")
            word = wav_file.stem.split('_', 1)[1] if '_' in wav_file.stem else wav_file.stem
            
            recordings.append(RecordingInfo(
                filename=wav_file.name,
                word=word,
                audio_path=f"/audio/{participant_id}/{wav_file.name}",
                labeled=labeled,
                score=score,
                evaluator=evaluator,
                notes=notes,
                timestamp=timestamp
            ))
    
    return {
        "participant_id": participant_id,
        "info": participant_info,
        "survey": survey_data,
        "recordings": recordings,
        "stats": {
            "total_recordings": len(recordings),
            "labeled": sum(1 for r in recordings if r.labeled),
            "unlabeled": sum(1 for r in recordings if not r.labeled)
        }
    }


@router.post("/label/{participant_id}/{filename}")
async def save_label(participant_id: str, filename: str, label: LabelData):
    """
    Save label/score for a recording.
    
    Args:
        participant_id: Participant ID
        filename: Recording filename (e.g., "01_araba.wav")
        label: Label data with score and notes
    
    Returns:
        Success message
    """
    participant_dir = DATA_DIR / participant_id
    
    if not participant_dir.exists():
        raise HTTPException(status_code=404, detail="Participant not found")
    
    kelimeler_dir = participant_dir / "kelimeler"
    if not kelimeler_dir.exists():
        raise HTTPException(status_code=404, detail="Recordings directory not found")
    
    # Check if audio file exists
    audio_file = kelimeler_dir / filename
    if not audio_file.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    # Create result file
    result_filename = f"{audio_file.stem}_result.json"
    result_file = kelimeler_dir / result_filename
    
    # Prepare label data
    label_data = {
        "word": label.word,
        "score": label.score,
        "labeled": True,
        "evaluator": label.evaluator,
        "notes": label.notes,
        "timestamp": label.timestamp or datetime.now().isoformat(),
        "pronunciation_quality": label.pronunciation_quality,
        "specific_issues": label.specific_issues
    }
    
    # Save to file
    try:
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(label_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Label saved: {result_file} (score: {label.score})")
        
        return {
            "success": True,
            "message": "Label saved successfully",
            "file": str(result_file)
        }
    except Exception as e:
        logger.error(f"Failed to save label: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save label: {str(e)}")


@router.get("/label/{participant_id}/{filename}")
async def get_label(participant_id: str, filename: str):
    """
    Get existing label for a recording.
    
    Args:
        participant_id: Participant ID
        filename: Recording filename
    
    Returns:
        Label data if exists, None otherwise
    """
    participant_dir = DATA_DIR / participant_id
    
    if not participant_dir.exists():
        raise HTTPException(status_code=404, detail="Participant not found")
    
    kelimeler_dir = participant_dir / "kelimeler"
    audio_file = kelimeler_dir / filename
    
    if not audio_file.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    result_file = audio_file.parent / f"{audio_file.stem}_result.json"
    
    if not result_file.exists():
        return {"labeled": False}
    
    try:
        with open(result_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error reading label: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to read label: {str(e)}")


@router.delete("/label/{participant_id}/{filename}")
async def delete_label(participant_id: str, filename: str):
    """
    Delete a label (e.g., to re-label).
    
    Args:
        participant_id: Participant ID
        filename: Recording filename
    
    Returns:
        Success message
    """
    participant_dir = DATA_DIR / participant_id
    kelimeler_dir = participant_dir / "kelimeler"
    audio_file = kelimeler_dir / filename
    
    if not audio_file.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    result_file = audio_file.parent / f"{audio_file.stem}_result.json"
    
    if result_file.exists():
        try:
            result_file.unlink()
            return {"success": True, "message": "Label deleted"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete label: {str(e)}")
    else:
        return {"success": True, "message": "No label to delete"}


@router.get("/stats")
async def get_labeling_stats():
    """
    Get overall labeling statistics.
    
    Returns:
        Global statistics about labeling progress
    """
    if not DATA_DIR.exists():
        return {
            "total_participants": 0,
            "total_recordings": 0,
            "labeled_recordings": 0,
            "unlabeled_recordings": 0,
            "labeling_progress": 0
        }
    
    total_participants = 0
    total_recordings = 0
    labeled_recordings = 0
    
    for participant_dir in DATA_DIR.glob("participant_*"):
        total_participants += 1
        
        kelimeler_dir = participant_dir / "kelimeler"
        if kelimeler_dir.exists():
            wav_files = list(kelimeler_dir.glob("*.wav"))
            total_recordings += len(wav_files)
            
            for wav_file in wav_files:
                result_file = wav_file.parent / f"{wav_file.stem}_result.json"
                if result_file.exists():
                    labeled_recordings += 1
    
    unlabeled_recordings = total_recordings - labeled_recordings
    progress = (labeled_recordings / total_recordings * 100) if total_recordings > 0 else 0
    
    return {
        "total_participants": total_participants,
        "total_recordings": total_recordings,
        "labeled_recordings": labeled_recordings,
        "unlabeled_recordings": unlabeled_recordings,
        "labeling_progress": round(progress, 1)
    }
