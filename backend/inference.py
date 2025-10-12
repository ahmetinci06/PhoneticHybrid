"""
Pronunciation Analysis and Inference Module
Analyzes recorded audio and compares with target phoneme sequences
"""

import librosa
import numpy as np
import parselmouth
from parselmouth.praat import call
from typing import Dict, List, Tuple, Optional
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
    Main function to analyze pronunciation quality of recorded audio.
    
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
            "grade": str
        }
        
    Example:
        >>> result = analyze_pronunciation("pencere.wav", "pencere", "p e n d͡ʒ e ɾ e")
        >>> print(result['overall'])
        0.84
    """
    logger.info(f"Analyzing pronunciation: word='{word}', audio='{audio_path}'")
    
    # Initialize analyzer
    analyzer = PronunciationAnalyzer()
    
    # Extract acoustic features
    features = analyzer.extract_acoustic_features(audio_path)
    
    # Compare with target phonemes
    phoneme_scores = analyzer.compare_phonemes(target_phonemes, features)
    
    # Calculate overall score
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
        "phoneme_count": len(phoneme_scores)
    }
    
    logger.info(f"Analysis complete: overall={overall_score:.3f}, grade={grade}")
    
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
