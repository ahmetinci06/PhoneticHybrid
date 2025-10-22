"""
Prepare training data for pronunciation scoring model.
Extracts features from recorded audio and creates labeled dataset.
"""

import json
import librosa
import numpy as np
import parselmouth
from parselmouth.praat import call
from pathlib import Path
import pandas as pd
from tqdm import tqdm
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_features_from_audio(audio_path: str, sample_rate: int = 16000) -> dict:
    """
    Extract comprehensive acoustic features for ML model.
    
    Args:
        audio_path: Path to .wav file
        sample_rate: Target sampling rate
        
    Returns:
        Dictionary with extracted features
    """
    try:
        # Load audio
        y, sr = librosa.load(audio_path, sr=sample_rate)
        duration = librosa.get_duration(y=y, sr=sr)
        
        # Skip very short audio
        if duration < 0.2:
            logger.warning(f"Audio too short: {audio_path} ({duration:.2f}s)")
            return None
        
        # 1. MFCCs (13 coefficients)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_mean = np.mean(mfcc, axis=1)
        mfcc_std = np.std(mfcc, axis=1)
        mfcc_delta = librosa.feature.delta(mfcc)
        mfcc_delta_mean = np.mean(mfcc_delta, axis=1)
        
        # 2. Pitch (F0)
        f0, voiced_flag, voiced_probs = librosa.pyin(
            y, 
            fmin=librosa.note_to_hz('C2'),
            fmax=librosa.note_to_hz('C7')
        )
        f0_clean = f0[~np.isnan(f0)]
        pitch_mean = np.mean(f0_clean) if len(f0_clean) > 0 else 0
        pitch_std = np.std(f0_clean) if len(f0_clean) > 0 else 0
        pitch_range = np.ptp(f0_clean) if len(f0_clean) > 0 else 0
        
        # 3. Formants via Praat
        try:
            sound = parselmouth.Sound(audio_path)
            formant = call(sound, "To Formant (burg)", 0.0, 5, 5500, 0.025, 50)
            
            f1_mean = call(formant, "Get mean", 1, 0, 0, 'Hertz')
            f2_mean = call(formant, "Get mean", 2, 0, 0, 'Hertz')
            f3_mean = call(formant, "Get mean", 3, 0, 0, 'Hertz')
            
            f1_std = call(formant, "Get standard deviation", 1, 0, 0, 'Hertz')
            f2_std = call(formant, "Get standard deviation", 2, 0, 0, 'Hertz')
        except Exception as e:
            logger.warning(f"Formant extraction failed for {audio_path}: {e}")
            f1_mean = f2_mean = f3_mean = 0
            f1_std = f2_std = 0
        
        # 4. Energy features
        rms = librosa.feature.rms(y=y)[0]
        energy_mean = np.mean(rms)
        energy_std = np.std(rms)
        energy_max = np.max(rms)
        
        # 5. Spectral features
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        spectral_flatness = librosa.feature.spectral_flatness(y=y)
        zero_crossing_rate = librosa.feature.zero_crossing_rate(y)
        
        # 6. Temporal features
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        
        # 7. Harmonic and percussive components
        y_harmonic, y_percussive = librosa.effects.hpss(y)
        harmonic_ratio = np.sum(y_harmonic**2) / (np.sum(y**2) + 1e-10)
        
        # Combine all features into a flat vector
        features = {
            'duration': duration,
            
            # MFCCs (13 mean + 13 std + 13 delta = 39 features)
            **{f'mfcc_{i}_mean': mfcc_mean[i] for i in range(13)},
            **{f'mfcc_{i}_std': mfcc_std[i] for i in range(13)},
            **{f'mfcc_{i}_delta': mfcc_delta_mean[i] for i in range(13)},
            
            # Pitch (3 features)
            'pitch_mean': pitch_mean,
            'pitch_std': pitch_std,
            'pitch_range': pitch_range,
            
            # Formants (5 features)
            'f1_mean': f1_mean,
            'f2_mean': f2_mean,
            'f3_mean': f3_mean,
            'f1_std': f1_std,
            'f2_std': f2_std,
            
            # Energy (3 features)
            'energy_mean': energy_mean,
            'energy_std': energy_std,
            'energy_max': energy_max,
            
            # Spectral (5 features)
            'spectral_centroid_mean': np.mean(spectral_centroid),
            'spectral_rolloff_mean': np.mean(spectral_rolloff),
            'spectral_bandwidth_mean': np.mean(spectral_bandwidth),
            'spectral_flatness_mean': np.mean(spectral_flatness),
            'zero_crossing_rate_mean': np.mean(zero_crossing_rate),
            
            # Temporal (1 feature)
            'tempo': tempo,
            
            # Harmonic (1 feature)
            'harmonic_ratio': harmonic_ratio,
        }
        
        return features
        
    except Exception as e:
        logger.error(f"Feature extraction failed for {audio_path}: {e}")
        return None


def prepare_dataset(data_dir: str, output_file: str = "training_data.csv"):
    """
    Prepare training dataset from collected participant data.
    
    Args:
        data_dir: Root directory containing participant folders
        output_file: Output CSV filename
        
    Expected structure:
        data_dir/
          participant_XXX/
            kelimeler/
              01_araba.wav
              01_araba_result.json  # Contains: {"score": 85, "word": "araba"}
              02_çocuk.wav
              02_çocuk_result.json
              ...
    """
    data_path = Path(data_dir)
    
    if not data_path.exists():
        logger.error(f"Data directory not found: {data_dir}")
        return
    
    # Collect all audio files and their labels
    dataset = []
    
    participant_dirs = list(data_path.glob("participant_*"))
    logger.info(f"Found {len(participant_dirs)} participant directories")
    
    for participant_dir in tqdm(participant_dirs, desc="Processing participants"):
        kelimeler_dir = participant_dir / "kelimeler"
        
        if not kelimeler_dir.exists():
            continue
        
        # Find all .wav files
        audio_files = list(kelimeler_dir.glob("*.wav"))
        
        for audio_file in audio_files:
            # Find corresponding result JSON
            result_file = audio_file.with_suffix('.wav').parent / f"{audio_file.stem}_result.json"
            
            if not result_file.exists():
                logger.warning(f"No result file for: {audio_file}")
                continue
            
            # Load label (score)
            try:
                with open(result_file, 'r', encoding='utf-8') as f:
                    result_data = json.load(f)
                    score = result_data.get('score')
                    word = result_data.get('word', audio_file.stem.split('_', 1)[1])
                    
                    if score is None:
                        logger.warning(f"No score in result file: {result_file}")
                        continue
                    
            except Exception as e:
                logger.error(f"Failed to load result file {result_file}: {e}")
                continue
            
            # Extract features
            features = extract_features_from_audio(str(audio_file))
            
            if features is None:
                continue
            
            # Add metadata
            features['word'] = word
            features['participant_id'] = participant_dir.name
            features['audio_file'] = str(audio_file)
            features['score'] = float(score)  # Target label
            
            dataset.append(features)
    
    if len(dataset) == 0:
        logger.error("No data collected! Check your data directory structure.")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(dataset)
    
    # Save to CSV
    output_path = Path(data_dir) / output_file
    df.to_csv(output_path, index=False)
    
    logger.info(f"Dataset created: {output_path}")
    logger.info(f"Total samples: {len(df)}")
    logger.info(f"Unique words: {df['word'].nunique()}")
    logger.info(f"Unique participants: {df['participant_id'].nunique()}")
    logger.info(f"Score range: {df['score'].min():.1f} - {df['score'].max():.1f}")
    logger.info(f"Score mean: {df['score'].mean():.1f} ± {df['score'].std():.1f}")
    logger.info(f"Features extracted: {len(df.columns) - 4}")  # Excluding metadata columns
    
    return df


def create_mock_labels(data_dir: str):
    """
    Create mock result.json files for existing audio files.
    Use this if you don't have labeled data yet.
    
    WARNING: This creates RANDOM scores for demonstration only!
    Replace with real human-labeled scores for production.
    """
    data_path = Path(data_dir)
    
    participant_dirs = list(data_path.glob("participant_*"))
    logger.info(f"Creating mock labels for {len(participant_dirs)} participants...")
    
    count = 0
    for participant_dir in participant_dirs:
        kelimeler_dir = participant_dir / "kelimeler"
        
        if not kelimeler_dir.exists():
            continue
        
        audio_files = list(kelimeler_dir.glob("*.wav"))
        
        for audio_file in audio_files:
            result_file = audio_file.with_suffix('.wav').parent / f"{audio_file.stem}_result.json"
            
            if result_file.exists():
                continue  # Don't overwrite existing labels
            
            # Extract word from filename (e.g., "01_araba.wav" -> "araba")
            word = audio_file.stem.split('_', 1)[1] if '_' in audio_file.stem else audio_file.stem
            
            # Create mock score (REPLACE THIS WITH REAL LABELS!)
            mock_score = np.random.uniform(60, 95)
            
            mock_data = {
                "word": word,
                "score": round(mock_score, 1),
                "labeled": False,  # Mark as mock
                "note": "This is a mock score for testing. Replace with real human evaluation."
            }
            
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(mock_data, f, ensure_ascii=False, indent=2)
            
            count += 1
    
    logger.info(f"Created {count} mock labels")
    logger.info("⚠️  NOW REPLACE THEM WITH REAL HUMAN-LABELED SCORES!")


if __name__ == "__main__":
    import sys
    
    # Default data directory
    data_dir = "../data"
    
    if len(sys.argv) > 1:
        data_dir = sys.argv[1]
    
    print("=" * 70)
    print("  Pronunciation ML Training - Data Preparation")
    print("=" * 70)
    
    choice = input("\n1. Create mock labels (for testing)\n2. Prepare dataset from existing labels\n\nChoice (1 or 2): ")
    
    if choice == "1":
        print("\n⚠️  WARNING: Creating MOCK labels with random scores!")
        print("   These are for testing only. Replace with real human evaluations.\n")
        confirm = input("Continue? (yes/no): ")
        if confirm.lower() == 'yes':
            create_mock_labels(data_dir)
            print("\n✅ Mock labels created in data/participant_*/kelimeler/*_result.json")
    
    elif choice == "2":
        print(f"\n📊 Preparing dataset from: {data_dir}")
        df = prepare_dataset(data_dir)
        
        if df is not None:
            print("\n✅ Dataset prepared successfully!")
            print(f"   Output: {data_dir}/training_data.csv")
            print(f"\n📈 Statistics:")
            print(f"   Samples: {len(df)}")
            print(f"   Features: {len([c for c in df.columns if c not in ['word', 'participant_id', 'audio_file', 'score']])}")
            print(f"   Score range: {df['score'].min():.1f} - {df['score'].max():.1f}")
    else:
        print("Invalid choice. Exiting.")
