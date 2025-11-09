"""
Phoneme Generation Service for Turkish Language
Uses Phonemizer library with eSpeak-NG backend
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging
import os
import platform
import subprocess

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI router
router = APIRouter(prefix="/phoneme", tags=["phoneme"])

# Global flag to track if phonemizer is available
phonemizer_available = False
espeak_exe_path = None

# Initialize eSpeak-NG and set library path for phonemizer
try:
    # Set eSpeak-NG library path for phonemizer
    if platform.system() == 'Darwin':  # macOS
        espeak_lib = '/opt/homebrew/opt/espeak-ng/lib/libespeak-ng.dylib'
        if os.path.exists(espeak_lib):
            os.environ['PHONEMIZER_ESPEAK_LIBRARY'] = espeak_lib
            logger.info(f"✓ Set PHONEMIZER_ESPEAK_LIBRARY to: {espeak_lib}")
        else:
            # Try Intel Mac location
            espeak_lib = '/usr/local/opt/espeak-ng/lib/libespeak-ng.dylib'
            if os.path.exists(espeak_lib):
                os.environ['PHONEMIZER_ESPEAK_LIBRARY'] = espeak_lib
                logger.info(f"✓ Set PHONEMIZER_ESPEAK_LIBRARY to: {espeak_lib}")
    elif platform.system() == 'Linux':
        possible_paths = [
            '/usr/lib/x86_64-linux-gnu/libespeak-ng.so',
            '/usr/lib/libespeak-ng.so',
            '/usr/local/lib/libespeak-ng.so'
        ]
        for lib_path in possible_paths:
            if os.path.exists(lib_path):
                os.environ['PHONEMIZER_ESPEAK_LIBRARY'] = lib_path
                logger.info(f"✓ Set PHONEMIZER_ESPEAK_LIBRARY to: {lib_path}")
                break

    if platform.system() == 'Windows':
        # Find eSpeak-NG executable
        espeak_dir = r"C:\Program Files\eSpeak NG"
        espeak_exe = os.path.join(espeak_dir, "espeak-ng.exe")

        if os.path.exists(espeak_exe):
            espeak_exe_path = espeak_exe
            logger.info(f"✓ Found eSpeak-NG at: {espeak_exe}")

            # Test if it works
            result = subprocess.run(
                [espeak_exe, "--version"],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                phonemizer_available = True
                version_info = result.stdout.decode('utf-8', errors='ignore').strip().split('\n')[0]
                logger.info("✓ eSpeak-NG is working and available for phoneme generation")
                logger.info(f"✓ Version: {version_info}")
            else:
                logger.warning("⚠ eSpeak-NG found but not responding correctly")
        else:
            logger.warning(f"⚠ eSpeak-NG not found at: {espeak_exe}")
    else:
        # Linux/Mac: Check if espeak-ng is in PATH
        result = subprocess.run(
            ["espeak-ng", "--version"],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            phonemizer_available = True
            espeak_exe_path = "espeak-ng"
            logger.info("✓ eSpeak-NG is available")

except Exception as e:
    logger.warning(f"⚠ Could not initialize eSpeak-NG: {e}")
    logger.warning("⚠ Phoneme service will not be available.")
    phonemizer_available = False


# Pydantic models
class PhonemeRequest(BaseModel):
    """Request model for phoneme generation"""
    word: str
    include_stress: bool = True
    separator: str = " "  # Space between phonemes


class PhonemeResponse(BaseModel):
    """Response model with phoneme data"""
    word: str
    phonemes: str
    phoneme_count: int
    language: str = "tr"
    backend: str = "espeak-ng"


class PhonemeAnalysis(BaseModel):
    """Detailed phoneme analysis"""
    word: str
    phonemes: str
    phoneme_list: list[str]
    phoneme_count: int
    syllable_estimate: Optional[int] = None
    language: str = "tr"


# API Endpoints

@router.post("/generate", response_model=PhonemeResponse)
async def generate_phonemes(request: PhonemeRequest):
    """
    Generate IPA phoneme sequence for a Turkish word.
    
    Args:
        request: PhonemeRequest with word and options
        
    Returns:
        PhonemeResponse with phoneme string
        
    Example:
        POST /phoneme/generate
        {
            "word": "pencere",
            "include_stress": true,
            "separator": " "
        }
        
        Response:
        {
            "word": "pencere",
            "phonemes": "p e n d͡ʒ e ɾ e",
            "phoneme_count": 7,
            "language": "tr",
            "backend": "espeak-ng"
        }
    """
    if not phonemizer_available or espeak_exe_path is None:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "eSpeak-NG not available",
                "message": "Phoneme service requires eSpeak-NG to be installed on your system.",
                "instructions": {
                    "windows": "Download from: https://github.com/espeak-ng/espeak-ng/releases",
                    "alternative": "Use online IPA tools temporarily"
                }
            }
        )
    
    if not request.word or not request.word.strip():
        raise HTTPException(
            status_code=400,
            detail="Word cannot be empty"
        )
    
    try:
        # Clean input
        word = request.word.strip()
        
        # Call eSpeak-NG directly using subprocess
        # -v tr = Turkish voice
        # -q = quiet (no audio)
        # --ipa = output IPA phonemes
        result = subprocess.run(
            [espeak_exe_path, "-v", "tr", "-q", "--ipa", word],
            capture_output=True,
            timeout=5
        )
        
        if result.returncode != 0:
            error_msg = result.stderr.decode('utf-8', errors='ignore') if result.stderr else 'Unknown error'
            raise Exception(f"eSpeak-NG returned error: {error_msg}")
        
        # Decode output as UTF-8 bytes (more reliable on Windows)
        phonemes_raw = result.stdout.decode('utf-8', errors='ignore').strip()
        
        # Split into individual phonemes and join with specified separator
        # eSpeak-NG already provides IPA symbols
        phoneme_list = [p.strip() for p in phonemes_raw if p.strip() and p not in ['\n', '\r', '\t']]
        
        # Join with separator if requested
        if request.separator:
            phonemes = request.separator.join(phonemes_raw.replace('\n', '').replace('\r', '').strip().split())
        else:
            phonemes = phonemes_raw.replace('\n', ' ').replace('\r', '').strip()
        
        # Count actual phonemes (split by space)
        phoneme_count = len([p for p in phonemes.split() if p])
        
        logger.info(f"Generated phonemes for '{word}': {phonemes}")
        
        return PhonemeResponse(
            word=word,
            phonemes=phonemes,
            phoneme_count=phoneme_count,
            language="tr",
            backend="espeak-ng"
        )
    
    except subprocess.TimeoutExpired:
        logger.error(f"eSpeak-NG timeout for word: {request.word}")
        raise HTTPException(
            status_code=500,
            detail="Phoneme generation timed out"
        )
    except Exception as e:
        logger.error(f"Phoneme generation failed for '{request.word}': {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Phoneme generation failed: {str(e)}"
        )


@router.post("/analyze", response_model=PhonemeAnalysis)
async def analyze_phonemes(request: PhonemeRequest):
    """
    Detailed phoneme analysis for a Turkish word.
    
    Returns phoneme string, list, and additional analysis.
    """
    if not phonemizer_available or espeak_exe_path is None:
        raise HTTPException(
            status_code=503,
            detail="eSpeak-NG backend not available"
        )
    
    if not request.word or not request.word.strip():
        raise HTTPException(
            status_code=400,
            detail="Word cannot be empty"
        )
    
    try:
        word = request.word.strip()
        
        # Call eSpeak-NG directly
        result = subprocess.run(
            [espeak_exe_path, "-v", "tr", "-q", "--ipa", word],
            capture_output=True,
            timeout=5
        )
        
        if result.returncode != 0:
            error_msg = result.stderr.decode('utf-8', errors='ignore') if result.stderr else 'Unknown error'
            raise Exception(f"eSpeak-NG error: {error_msg}")
        
        phonemes_raw = result.stdout.decode('utf-8', errors='ignore').strip()
        phonemes = request.separator.join(phonemes_raw.replace('\n', '').replace('\r', '').strip().split())
        
        # Parse phoneme list
        phoneme_list = [p for p in phonemes.split(request.separator) if p]
        phoneme_count = len(phoneme_list)
        
        # Estimate syllables (count vowels in IPA)
        turkish_vowels = set('aeɛioœuyɯø')
        syllable_estimate = sum(1 for p in phoneme_list if any(v in p for v in turkish_vowels))
        
        return PhonemeAnalysis(
            word=word,
            phonemes=phonemes,
            phoneme_list=phoneme_list,
            phoneme_count=phoneme_count,
            syllable_estimate=syllable_estimate,
            language="tr"
        )
    
    except Exception as e:
        logger.error(f"Phoneme analysis failed for '{request.word}': {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Phoneme analysis failed: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Check if phoneme service is available"""
    if not phonemizer_available or espeak_exe_path is None:
        return {
            "status": "unavailable",
            "backend": "espeak-ng",
            "message": "eSpeak-NG not initialized"
        }
    
    # Get version from espeak-ng
    try:
        result = subprocess.run(
            [espeak_exe_path, "--version"],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            version_line = result.stdout.decode('utf-8', errors='ignore').strip().split('\n')[0]
        else:
            version_line = "unknown"
    except:
        version_line = "unknown"
    
    return {
        "status": "available",
        "backend": "espeak-ng",
        "language": "tr",
        "version": version_line
    }


@router.post("/batch", response_model=list[PhonemeResponse])
async def generate_batch_phonemes(words: list[str]):
    """
    Generate phonemes for multiple words at once.
    
    Useful for batch processing in ML training pipeline.
    
    Args:
        words: List of Turkish words
        
    Returns:
        List of PhonemeResponse objects
    """
    if not phonemizer_available or espeak_exe_path is None:
        raise HTTPException(
            status_code=503,
            detail="eSpeak-NG backend not available"
        )
    
    if not words or len(words) == 0:
        raise HTTPException(
            status_code=400,
            detail="Word list cannot be empty"
        )
    
    try:
        results = []
        
        for word in words:
            if not word.strip():
                continue
            
            # Call eSpeak-NG for each word
            result = subprocess.run(
                [espeak_exe_path, "-v", "tr", "-q", "--ipa", word.strip()],
                capture_output=True,
                timeout=5
            )
            
            if result.returncode == 0:
                phonemes_raw = result.stdout.decode('utf-8', errors='ignore').strip()
                phonemes = ' '.join(phonemes_raw.replace('\n', '').replace('\r', '').strip().split())
                phoneme_list = [p for p in phonemes.split(' ') if p]
                
                results.append(PhonemeResponse(
                    word=word.strip(),
                    phonemes=phonemes,
                    phoneme_count=len(phoneme_list),
                    language="tr",
                    backend="espeak-ng"
                ))
        
        return results
    
    except Exception as e:
        logger.error(f"Batch phoneme generation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Batch processing failed: {str(e)}"
        )
