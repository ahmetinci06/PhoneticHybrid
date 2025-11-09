"""
Pronunciation Analysis and Inference Module
Analyzes recorded audio and compares with target phoneme sequences

This module uses Whisper (OpenAI open-source) for speech recognition
combined with phoneme analysis for production-ready pronunciation evaluation.
"""

import librosa
import numpy as np
import parselmouth
from parselmouth.praat import call
from typing import Dict, List, Tuple, Optional
import logging
from pathlib import Path
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load Whisper model once at module level (one-time initialization)
# This prevents reloading the model on each function call, improving performance
_whisper_model = None

def _get_whisper_model():
    """Lazy load Whisper model on first use."""
    global _whisper_model
    if _whisper_model is None:
        try:
            import whisper
            logger.info("Loading Whisper model (base) - this may take a minute on first run...")
            _whisper_model = whisper.load_model("base")
            logger.info("Whisper model loaded successfully")
        except ImportError:
            raise ImportError("openai-whisper not installed. Install with: pip install openai-whisper")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            raise
    return _whisper_model


class PronunciationAnalyzer:
    """
    Analyzes pronunciation quality by comparing acoustic features
    of recorded audio with expected phoneme sequences.
    """
    
    def __init__(self, sample_rate: int = 16000):
        """
        Initialize analyzer with target sample rate.
        
        Args:
            sample_rate: Target sampling rate for audio processing
        """
        self.sample_rate = sample_rate
        self.n_mfcc = 13
        
        # Turkish phoneme characteristics (approximate formant ranges in Hz)
        # These are simplified reference values for Turkish vowels
        self.turkish_vowel_formants = {
            'a': {'F1': 800, 'F2': 1300},
            'e': {'F1': 550, 'F2': 1900},
            'ɛ': {'F1': 650, 'F2': 1800},
            'i': {'F1': 300, 'F2': 2300},
            'o': {'F1': 500, 'F2': 900},
            'u': {'F1': 350, 'F2': 800},
            'y': {'F1': 300, 'F2': 1800},
            'ɯ': {'F1': 400, 'F2': 1200},
            'ø': {'F1': 450, 'F2': 1500},
        }
    
    def extract_acoustic_features(self, audio_path: str) -> Dict:
        """
        Extract comprehensive acoustic features from audio file.
        
        Args:
            audio_path: Path to .wav audio file
            
        Returns:
            Dictionary containing MFCCs, pitch, formants, energy, duration
        """
        try:
            # Load audio with librosa
            y, sr = librosa.load(audio_path, sr=self.sample_rate)
            duration = librosa.get_duration(y=y, sr=sr)
            
            # 1. Extract MFCCs (Mel-frequency cepstral coefficients)
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=self.n_mfcc)
            mfcc_mean = np.mean(mfcc, axis=1)
            mfcc_std = np.std(mfcc, axis=1)
            
            # 2. Extract pitch (F0) using librosa
            f0, voiced_flag, voiced_probs = librosa.pyin(
                y, 
                fmin=librosa.note_to_hz('C2'),  # ~65 Hz
                fmax=librosa.note_to_hz('C7')   # ~2093 Hz
            )
            f0_clean = f0[~np.isnan(f0)]
            pitch_mean = np.mean(f0_clean) if len(f0_clean) > 0 else 0
            pitch_std = np.std(f0_clean) if len(f0_clean) > 0 else 0
            
            # 3. Extract formants using Praat (more accurate for phonetics)
            formants = self._extract_formants_praat(audio_path)
            
            # 4. Extract energy (RMS)
            rms = librosa.feature.rms(y=y)[0]
            energy_mean = np.mean(rms)
            energy_std = np.std(rms)
            
            # 5. Spectral features
            spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
            spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))
            zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(y))
            
            features = {
                'duration': float(duration),
                'mfcc_mean': mfcc_mean.tolist(),
                'mfcc_std': mfcc_std.tolist(),
                'pitch_mean': float(pitch_mean),
                'pitch_std': float(pitch_std),
                'formants': formants,
                'energy_mean': float(energy_mean),
                'energy_std': float(energy_std),
                'spectral_centroid': float(spectral_centroid),
                'spectral_rolloff': float(spectral_rolloff),
                'zero_crossing_rate': float(zero_crossing_rate),
            }
            
            logger.info(f"Extracted features from {audio_path}: duration={duration:.2f}s, pitch={pitch_mean:.1f}Hz")
            return features
            
        except Exception as e:
            logger.error(f"Feature extraction failed: {e}")
            raise
    
    def _extract_formants_praat(self, audio_path: str) -> Dict:
        """
        Extract formant frequencies (F1, F2, F3) using Praat.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Dictionary with formant values
        """
        try:
            # Load sound with Parselmouth (Praat Python wrapper)
            sound = parselmouth.Sound(audio_path)
            
            # Create Formant object
            formant = call(sound, "To Formant (burg)", 0.0, 5, 5500, 0.025, 50)
            
            # Get formants at midpoint (simplified)
            midpoint = sound.duration / 2
            
            f1 = call(formant, "Get value at time", 1, midpoint, 'Hertz', 'Linear')
            f2 = call(formant, "Get value at time", 2, midpoint, 'Hertz', 'Linear')
            f3 = call(formant, "Get value at time", 3, midpoint, 'Hertz', 'Linear')
            
            # Get mean values across entire duration
            f1_mean = call(formant, "Get mean", 1, 0, 0, 'Hertz')
            f2_mean = call(formant, "Get mean", 2, 0, 0, 'Hertz')
            f3_mean = call(formant, "Get mean", 3, 0, 0, 'Hertz')
            
            return {
                'F1': float(f1) if not np.isnan(f1) else float(f1_mean),
                'F2': float(f2) if not np.isnan(f2) else float(f2_mean),
                'F3': float(f3) if not np.isnan(f3) else float(f3_mean),
                'F1_mean': float(f1_mean),
                'F2_mean': float(f2_mean),
                'F3_mean': float(f3_mean),
            }
            
        except Exception as e:
            logger.warning(f"Formant extraction with Praat failed: {e}")
            return {
                'F1': 0.0, 'F2': 0.0, 'F3': 0.0,
                'F1_mean': 0.0, 'F2_mean': 0.0, 'F3_mean': 0.0
            }
    
    def compare_phonemes(
        self, 
        target_phonemes: str, 
        features: Dict
    ) -> Dict[str, float]:
        """
        Compare extracted features with target phonemes.
        Compute per-phoneme pronunciation scores.
        
        Args:
            target_phonemes: Space-separated IPA phoneme string
            features: Extracted acoustic features
            
        Returns:
            Dictionary mapping phoneme -> score (0-1)
        """
        phoneme_list = [p for p in target_phonemes.split() if p.strip()]
        
        if not phoneme_list:
            return {}
        
        scores = {}
        
        # Simple heuristic scoring based on feature quality
        for phoneme in phoneme_list:
            score = self._score_phoneme(phoneme, features)
            scores[phoneme] = score
        
        return scores
    
    def _score_phoneme(self, phoneme: str, features: Dict) -> float:
        """
        Score a single phoneme based on acoustic features.
        Uses heuristic rules for demonstration.
        
        In production, replace with trained ML model.
        
        Args:
            phoneme: Single IPA phoneme character
            features: Acoustic features
            
        Returns:
            Score between 0.0 and 1.0
        """
        score = 0.7  # Base score
        
        # Check if it's a vowel
        if phoneme in self.turkish_vowel_formants:
            # Compare formants with expected ranges
            expected = self.turkish_vowel_formants[phoneme]
            
            if 'formants' in features and features['formants']['F1'] > 0:
                f1_actual = features['formants']['F1_mean']
                f2_actual = features['formants']['F2_mean']
                
                f1_expected = expected['F1']
                f2_expected = expected['F2']
                
                # Calculate normalized distance
                f1_error = abs(f1_actual - f1_expected) / f1_expected
                f2_error = abs(f2_actual - f2_expected) / f2_expected
                
                # Convert error to score (lower error = higher score)
                formant_score = 1.0 - min(1.0, (f1_error + f2_error) / 2)
                score = 0.3 * score + 0.7 * formant_score
        
        # Check consonant characteristics
        else:
            # For consonants, check energy and spectral features
            # Plosives (p, t, k, b, d, g) should have higher energy bursts
            if phoneme in ['p', 't', 'k', 'b', 'd', 'ɡ']:
                if features.get('energy_mean', 0) > 0.01:
                    score += 0.1
            
            # Fricatives (f, s, ʃ, v, z, ʒ, h) should have high frequency content
            if phoneme in ['f', 's', 'ʃ', 'v', 'z', 'ʒ', 'h']:
                if features.get('spectral_centroid', 0) > 2000:
                    score += 0.1
            
            # Nasals (m, n) should have lower frequencies
            if phoneme in ['m', 'n']:
                if features.get('spectral_centroid', 0) < 1500:
                    score += 0.1
        
        # Clip score to [0.3, 1.0] range
        score = max(0.3, min(1.0, score))
        
        return float(score)
    
    def calculate_overall_score(self, phoneme_scores: Dict[str, float]) -> float:
        """
        Calculate overall pronunciation quality score.
        
        Args:
            phoneme_scores: Dictionary of phoneme -> score
            
        Returns:
            Overall score (0-1)
        """
        if not phoneme_scores:
            return 0.0
        
        scores = list(phoneme_scores.values())
        
        # Weighted average (penalize low scores more)
        mean_score = np.mean(scores)
        min_score = np.min(scores)
        
        # 70% mean, 30% minimum (to penalize poor phonemes)
        overall = 0.7 * mean_score + 0.3 * min_score
        
        return float(overall)


def analyze_pronunciation(audio_path: str, word: str, target_phonemes: str) -> Dict:
    """
    DEPRECATED: Use analyze_pronunciation_whisper() instead for production.

    Legacy function for heuristic-based pronunciation analysis.
    Kept for backward compatibility and phoneme extraction testing.
    
    Args:
        audio_path: Path to recorded .wav file
        word: Target word being pronounced
        target_phonemes: Expected phoneme sequence (IPA, space-separated)
        
    Returns:
        Dictionary with analysis results:
        {
            "word": str,
            "phonemes_target": str,
            "features": dict,
            "scores": dict,
            "overall": float,
            "grade": str,
            "scoring_method": str
        }
        
    Example:
        >>> result = analyze_pronunciation("pencere.wav", "pencere", "p e n d͡ʒ e ɾ e")
        >>> print(result['overall'])
        84.5
    """
    logger.info(f"Analyzing pronunciation: word='{word}', audio='{audio_path}'")
    
    # Initialize analyzer
    analyzer = PronunciationAnalyzer()
    
    # Extract acoustic features
    features = analyzer.extract_acoustic_features(audio_path)
    
    # Use heuristic scoring (deprecated - use Whisper API for production)
    logger.info("Using legacy heuristic scoring. Consider using analyze_pronunciation_whisper() for production.")
    scoring_method = "heuristic_legacy"
    phoneme_scores = analyzer.compare_phonemes(target_phonemes, features)
    overall_score = analyzer.calculate_overall_score(phoneme_scores)
    
    # Assign letter grade
    if overall_score >= 0.9:
        grade = "A (Mükemmel)"
    elif overall_score >= 0.8:
        grade = "B (İyi)"
    elif overall_score >= 0.7:
        grade = "C (Orta)"
    elif overall_score >= 0.6:
        grade = "D (Geliştirilebilir)"
    else:
        grade = "F (Zayıf)"
    
    result = {
        "word": word,
        "phonemes_target": target_phonemes,
        "features": {
            "duration": features['duration'],
            "pitch_mean": features['pitch_mean'],
            "formants": features['formants'],
        },
        "scores": phoneme_scores,
        "overall": round(overall_score, 3),
        "grade": grade,
        "phoneme_count": len(phoneme_scores),
        "scoring_method": scoring_method
    }
    
    logger.info(f"Analysis complete: overall={overall_score:.3f}, grade={grade}, method={scoring_method}")
    
    return result


def batch_analyze(audio_files: List[Tuple[str, str, str]]) -> List[Dict]:
    """
    Analyze multiple audio files in batch.
    
    Args:
        audio_files: List of (audio_path, word, target_phonemes) tuples
        
    Returns:
        List of analysis result dictionaries
    """
    results = []
    
    for audio_path, word, target_phonemes in audio_files:
        try:
            result = analyze_pronunciation(audio_path, word, target_phonemes)
            results.append(result)
        except Exception as e:
            logger.error(f"Failed to analyze {audio_path}: {e}")
            results.append({
                "word": word,
                "error": str(e),
                "overall": 0.0
            })
    
    return results


def analyze_pronunciation_whisper(audio_path: str, word: str) -> Dict:
    """
    Analyze pronunciation using Whisper (OpenAI open-source) combined with phoneme alignment.

    This production approach combines:
    1. Whisper speech-to-text for recognition (local, no API calls)
    2. Phonemizer (eSpeak NG) for ground-truth phoneme sequences
    3. Acoustic feature extraction (librosa, Praat) for detailed scoring
    4. Phoneme alignment for segment-level scores

    Args:
        audio_path: Path to recorded .wav audio file
        word: Target word being pronounced

    Returns:
        Dictionary with comprehensive analysis results:
        {
            "word": str,
            "recognized_text": str,
            "recognition_confidence": float,
            "phonemes_target": str,
            "segment_scores": dict,  # Phoneme -> score mapping
            "overall": float,
            "features": dict,
            "analysis_method": "whisper_hybrid"
        }

    Raises:
        ImportError: If required packages not installed
        Exception: If analysis fails
    """
    try:
        # Import required modules
        from phonemizer import phonemize
        from scipy.spatial.distance import euclidean
        from scipy.signal import resample

        logger.info(f"Starting Whisper-based analysis for word='{word}', audio='{audio_path}'")

        # Step 1: Recognize speech using Whisper
        recognized_text, whisper_confidence = _recognize_speech_whisper(audio_path, word)
        logger.info(f"Whisper recognition: '{recognized_text}' (confidence: {whisper_confidence:.2f})")

        # Step 2: Generate target phoneme sequence using Phonemizer
        target_phonemes = _generate_phonemes_espeak(word)
        logger.info(f"Target phonemes: {target_phonemes}")

        # Step 3: Extract acoustic features
        analyzer = PronunciationAnalyzer()
        features = analyzer.extract_acoustic_features(audio_path)

        # Step 3.5: Validate audio quality and word matching
        validation_passed, validation_score, validation_message = _validate_pronunciation_attempt(
            features=features,
            recognized_text=recognized_text,
            target_word=word
        )

        if not validation_passed:
            # Return low score with validation message
            logger.warning(f"Validation failed: {validation_message}")
            return {
                "word": word,
                "recognized_text": recognized_text,
                "recognition_confidence": round(whisper_confidence, 3),
                "phonemes_target": target_phonemes,
                "segment_scores": {},
                "overall": round(validation_score, 3),
                "grade": "F (Zayıf)",
                "features": {
                    "duration": features['duration'],
                    "pitch_mean": features['pitch_mean'],
                    "formants": features['formants'],
                },
                "analysis_method": "whisper_hybrid",
                "phoneme_count": 0,
                "validation_error": validation_message
            }

        # Step 4: Compute phoneme-wise alignment and scoring
        segment_scores = _compute_phoneme_alignment_scores(
            audio_path=audio_path,
            target_phonemes=target_phonemes,
            features=features,
            recognized_text=recognized_text
        )

        # Step 5: Calculate overall score
        # Combine Whisper confidence with acoustic-based scores
        # Factor in validation score to penalize mismatches
        acoustic_score = np.mean(list(segment_scores.values())) if segment_scores else 0.7
        base_score = 0.3 * whisper_confidence + 0.5 * acoustic_score + 0.2 * validation_score
        overall_score = base_score

        # Assign grade
        if overall_score >= 0.9:
            grade = "A (Mükemmel)"
        elif overall_score >= 0.8:
            grade = "B (İyi)"
        elif overall_score >= 0.7:
            grade = "C (Orta)"
        elif overall_score >= 0.6:
            grade = "D (Geliştirilebilir)"
        else:
            grade = "F (Zayıf)"

        result = {
            "word": word,
            "recognized_text": recognized_text,
            "recognition_confidence": round(whisper_confidence, 3),
            "phonemes_target": target_phonemes,
            "segment_scores": {k: round(v, 3) for k, v in segment_scores.items()},
            "overall": round(overall_score, 3),
            "grade": grade,
            "features": {
                "duration": features['duration'],
                "pitch_mean": features['pitch_mean'],
                "formants": features['formants'],
            },
            "analysis_method": "whisper_hybrid",
            "phoneme_count": len(segment_scores)
        }

        logger.info(f"Analysis complete: overall={overall_score:.3f}, grade={grade}")
        return result

    except ImportError as e:
        logger.error(f"Missing required package: {e}")
        raise ImportError(
            f"Required package not installed: {e}. "
            "Install with: pip install openai-whisper phonemizer scipy"
        )
    except Exception as e:
        logger.error(f"Whisper analysis failed: {e}")
        raise Exception(f"Pronunciation analysis failed: {str(e)}")


def _validate_pronunciation_attempt(
    features: Dict,
    recognized_text: str,
    target_word: str
) -> Tuple[bool, float, str]:
    """
    Validate if the pronunciation attempt is valid for scoring.

    Checks:
    1. Audio contains sufficient speech energy
    2. Recognized text reasonably matches target word
    3. Audio duration is appropriate

    Args:
        features: Acoustic features extracted from audio
        recognized_text: Text recognized by Whisper
        target_word: Expected word

    Returns:
        Tuple of (passed: bool, score: float, message: str)
    """
    # Validation 1: Check if audio contains speech (energy check)
    energy = features.get('energy_mean', 0)
    if energy < 0.001:  # Very low energy threshold
        return False, 0.0, "Ses seviyesi çok düşük - konuşma algılanamadı (No speech detected - audio too quiet)"

    # Validation 2: Check duration is reasonable (0.3s to 5s)
    duration = features.get('duration', 0)
    if duration < 0.3:
        return False, 0.1, "Ses kaydı çok kısa (Audio too short)"
    if duration > 5.0:
        return False, 0.2, "Ses kaydı çok uzun (Audio too long)"

    # Validation 3: Check word matching
    if not recognized_text or len(recognized_text.strip()) == 0:
        return False, 0.0, "Konuşma tanınamadı (Speech not recognized)"

    # Calculate similarity between recognized and target
    target_lower = target_word.lower().strip()
    recognized_lower = recognized_text.lower().strip()

    # Exact match - perfect
    if target_lower == recognized_lower:
        return True, 1.0, "Perfect match"

    # Check if one contains the other
    if target_lower in recognized_lower or recognized_lower in target_lower:
        return True, 0.9, "Partial match"

    # Character-level similarity using Levenshtein-like distance
    max_len = max(len(target_lower), len(recognized_lower))
    if max_len == 0:
        return False, 0.0, "Empty word detected"

    # Count common characters
    common = sum(1 for c in target_lower if c in recognized_lower)
    similarity = common / max_len

    # Threshold: require at least 40% character overlap
    if similarity < 0.4:
        return False, 0.3, f"Kelime uyuşmuyor: '{recognized_text}' != '{target_word}' (Word mismatch: recognized '{recognized_text}' instead of '{target_word}')"

    # Validation passed with reduced score for partial match
    validation_score = 0.5 + 0.5 * similarity
    return True, validation_score, f"Partial word match (similarity: {similarity:.0%})"


def _recognize_speech_whisper(audio_path: str, target_word: str = "") -> Tuple[str, float]:
    """
    Recognize speech using OpenAI Whisper (open-source, local).
    Uses multi-language fallback for better handling of Latin/English medical terms.

    Args:
        audio_path: Path to audio file
        target_word: Optional target word for confidence calculation

    Returns:
        Tuple of (recognized_text, confidence_score)
    """
    try:
        # Get the Whisper model (loads on first call, cached thereafter)
        model = _get_whisper_model()

        # Detect if target word is likely Latin/English (contains non-Turkish letters or patterns)
        is_likely_latin = False
        if target_word:
            latin_indicators = ['x', 'q', 'w', 'mandibula', 'maxilla', 'temporomandibular']
            target_lower = target_word.lower()
            is_likely_latin = any(ind in target_lower for ind in latin_indicators)

        # Strategy 1: Try with Turkish language (default for Turkish pronunciation tests)
        initial_prompt = f"Pronunciation test word: {target_word}" if target_word else ""

        result_tr = model.transcribe(
            audio_path,
            language="tr",  # Turkish
            task="transcribe",
            fp16=False,  # CPU compatibility
            initial_prompt=initial_prompt  # Help guide recognition
        )

        recognized_text = result_tr["text"].strip().lower()
        confidence = 0.85  # Default for successful recognition

        # If target word provided, try improving recognition
        if target_word and recognized_text:
            target_lower = target_word.lower().strip()

            # Check exact match
            if target_lower == recognized_text:
                confidence = 0.95
            # Check if words are contained in each other
            elif target_lower in recognized_text or recognized_text in target_lower:
                confidence = 0.90
            # Check character-level similarity (Levenshtein-like)
            else:
                # Calculate character overlap
                common_chars = sum(1 for c in target_lower if c in recognized_text)
                max_len = max(len(target_lower), len(recognized_text))
                char_similarity = common_chars / max_len if max_len > 0 else 0

                # If similarity is low and word might be Latin, try without language constraint
                if char_similarity < 0.5 and (is_likely_latin or len(recognized_text) <= 3):
                    logger.info(f"Low similarity ({char_similarity:.2f}), trying multilingual detection...")

                    result_multi = model.transcribe(
                        audio_path,
                        task="transcribe",
                        fp16=False,
                        initial_prompt=initial_prompt
                    )

                    recognized_multi = result_multi["text"].strip().lower()

                    # Calculate similarity for multilingual attempt
                    common_chars_multi = sum(1 for c in target_lower if c in recognized_multi)
                    multi_similarity = common_chars_multi / max_len if max_len > 0 else 0

                    # Use whichever has better similarity
                    if multi_similarity > char_similarity:
                        logger.info(f"Multilingual recognition better: '{recognized_multi}' (similarity: {multi_similarity:.2f})")
                        recognized_text = recognized_multi
                        char_similarity = multi_similarity

                confidence = 0.5 + 0.4 * char_similarity

        logger.info(f"Whisper recognized: '{recognized_text}' (confidence: {confidence:.2f})")
        return recognized_text, confidence

    except Exception as e:
        logger.error(f"Whisper recognition failed: {e}")
        return "", 0.0


def _generate_phonemes_espeak(word: str, language: str = "tr") -> str:
    """
    Generate phoneme sequence using Phonemizer (eSpeak NG backend).

    Args:
        word: Target word
        language: Language code (default: Turkish)

    Returns:
        Space-separated IPA phoneme string
    """
    try:
        from phonemizer import phonemize
        import platform
        import os

        # Configure eSpeak-NG library path for phonemizer
        # This is critical for macOS/Linux where phonemizer needs the library path
        if platform.system() == 'Darwin':  # macOS
            # Set library path for Homebrew-installed espeak-ng
            espeak_lib = '/opt/homebrew/opt/espeak-ng/lib/libespeak-ng.dylib'
            if os.path.exists(espeak_lib):
                os.environ['PHONEMIZER_ESPEAK_LIBRARY'] = espeak_lib
            else:
                # Try alternate location (Intel Mac)
                espeak_lib = '/usr/local/opt/espeak-ng/lib/libespeak-ng.dylib'
                if os.path.exists(espeak_lib):
                    os.environ['PHONEMIZER_ESPEAK_LIBRARY'] = espeak_lib
        elif platform.system() == 'Linux':
            # Linux typically has espeak-ng in standard library paths
            # But we can set it explicitly if needed
            possible_paths = [
                '/usr/lib/x86_64-linux-gnu/libespeak-ng.so',
                '/usr/lib/libespeak-ng.so',
                '/usr/local/lib/libespeak-ng.so'
            ]
            for lib_path in possible_paths:
                if os.path.exists(lib_path):
                    os.environ['PHONEMIZER_ESPEAK_LIBRARY'] = lib_path
                    break

        # Use phonemize with string backend name (NOT a backend object)
        phonemes = phonemize(
            word,
            language=language,
            backend='espeak',  # String backend name, not object
            strip=True,
            preserve_punctuation=False,
            with_stress=False
        )

        # Clean up the output - phonemizer returns space-separated phonemes
        phonemes = phonemes.strip()

        logger.info(f"Phonemizer output for '{word}': {phonemes}")
        return phonemes

    except Exception as e:
        logger.error(f"Phoneme generation failed: {e}")
        # Fallback to simple character split
        return " ".join(list(word))


def _compute_phoneme_alignment_scores(
    audio_path: str,
    target_phonemes: str,
    features: Dict,
    recognized_text: str
) -> Dict[str, float]:
    """
    Compute per-phoneme pronunciation scores using simplified alignment.
    
    This uses a combination of:
    - Text matching (recognized vs target)
    - Acoustic feature analysis per phoneme
    - Temporal alignment estimation
    
    Args:
        audio_path: Path to audio file
        target_phonemes: Target phoneme sequence (space-separated)
        features: Extracted acoustic features
        recognized_text: Text recognized by speech recognition
        
    Returns:
        Dictionary mapping each phoneme to a score (0-1)
    """
    phoneme_list = [p for p in target_phonemes.split() if p.strip()]
    
    if not phoneme_list:
        return {}
    
    scores = {}
    
    # Create analyzer instance
    analyzer = PronunciationAnalyzer()
    
    # Simple approach: Score each phoneme based on overall acoustic quality
    # In a production system, you'd use forced alignment (e.g., Montreal Forced Aligner)
    
    for phoneme in phoneme_list:
        # Base score from acoustic features
        base_score = analyzer._score_phoneme(phoneme, features)
        
        # Bonus if the phoneme's character appears in recognized text
        # (very simplified - production would use proper alignment)
        char = phoneme[0] if phoneme else ''
        if char and char in recognized_text:
            base_score = min(1.0, base_score + 0.05)
        
        scores[phoneme] = base_score
    
    return scores
