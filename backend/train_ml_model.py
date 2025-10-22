"""
Quick start script for ML model training workflow.
Guides user through data preparation and model deployment.
"""

import sys
from pathlib import Path
import subprocess


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def print_step(number, text):
    """Print step number"""
    print(f"\n{'='*70}")
    print(f"  STEP {number}: {text}")
    print(f"{'='*70}\n")


def check_data_directory():
    """Check if data directory exists and has participants"""
    data_dir = Path("../data")
    if not data_dir.exists():
        print("❌ Data directory not found: ../data")
        print("   Please ensure you have collected audio recordings first.")
        return False
    
    participants = list(data_dir.glob("participant_*"))
    if len(participants) == 0:
        print("❌ No participant directories found in ../data")
        print("   Use the frontend to collect recordings first.")
        return False
    
    print(f"✓ Found {len(participants)} participant directories")
    
    # Count audio files
    total_audio = 0
    total_labels = 0
    for p in participants:
        kelimeler = p / "kelimeler"
        if kelimeler.exists():
            audio_files = list(kelimeler.glob("*.wav"))
            label_files = list(kelimeler.glob("*_result.json"))
            total_audio += len(audio_files)
            total_labels += len(label_files)
    
    print(f"✓ Found {total_audio} audio files")
    print(f"✓ Found {total_labels} label files")
    
    if total_audio == 0:
        print("❌ No audio files found")
        return False
    
    if total_labels == 0:
        print("⚠️  No label files found - you'll need to create them")
    
    return True


def prepare_data():
    """Run data preparation script"""
    print("Starting data preparation...")
    print("\n" + "-" * 70)
    
    try:
        subprocess.run([sys.executable, "prepare_training_data.py"], check=True)
        return True
    except subprocess.CalledProcessError:
        print("\n❌ Data preparation failed")
        return False
    except FileNotFoundError:
        print("\n❌ prepare_training_data.py not found")
        return False


def check_training_csv():
    """Check if training data CSV was created"""
    csv_path = Path("../data/training_data.csv")
    if csv_path.exists():
        import pandas as pd
        try:
            df = pd.read_csv(csv_path)
            print(f"\n✓ Training data created: {len(df)} samples")
            print(f"  File: {csv_path}")
            return True
        except Exception as e:
            print(f"\n❌ Error reading CSV: {e}")
            return False
    else:
        print("\n❌ training_data.csv not created")
        return False


def check_model_files():
    """Check if model files exist in models directory"""
    models_dir = Path("models")
    
    required_files = [
        "pronunciation_scorer.pth",
        "model_info.json",
        "scaler_params.json"
    ]
    
    if not models_dir.exists():
        print(f"⚠️  Models directory not found: {models_dir}")
        return False
    
    missing = []
    for file in required_files:
        if not (models_dir / file).exists():
            missing.append(file)
    
    if missing:
        print(f"⚠️  Missing model files:")
        for f in missing:
            print(f"   - {f}")
        return False
    
    print(f"✓ All model files found in {models_dir}")
    return True


def test_ml_model():
    """Test if ML model loads correctly"""
    try:
        from ml_scorer import get_ml_scorer
        
        scorer = get_ml_scorer()
        
        if scorer and scorer.is_available():
            print("✓ ML model loaded successfully")
            return True
        else:
            print("❌ ML model failed to load")
            return False
            
    except Exception as e:
        print(f"❌ Error loading ML model: {e}")
        return False


def main():
    """Main workflow"""
    print_header("PhoneticHybrid - ML Model Training Workflow")
    
    print("This script will guide you through:")
    print("  1. Data preparation")
    print("  2. Model training (Google Colab)")
    print("  3. Model deployment")
    print()
    
    # Step 1: Check data
    print_step(1, "Check Data Directory")
    if not check_data_directory():
        print("\n❌ Setup incomplete. Please collect audio data first.")
        sys.exit(1)
    
    # Step 2: Prepare dataset
    print_step(2, "Prepare Training Dataset")
    print("Options:")
    print("  1. Create mock labels (for testing)")
    print("  2. Prepare dataset from existing labels")
    print()
    
    if not prepare_data():
        print("\n❌ Data preparation failed")
        sys.exit(1)
    
    if not check_training_csv():
        print("\n❌ Training data not created")
        sys.exit(1)
    
    # Step 3: Training instructions
    print_step(3, "Train Model in Google Colab")
    print("📋 Next steps:")
    print()
    print("1. Open Google Colab:")
    print("   https://colab.research.google.com/")
    print()
    print("2. Upload this notebook:")
    print("   ml_colab/pronunciation_scoring_training.ipynb")
    print()
    print("3. Enable GPU:")
    print("   Runtime → Change runtime type → GPU")
    print()
    print("4. Upload training data:")
    print("   data/training_data.csv")
    print()
    print("5. Run all cells and wait for training to complete")
    print("   (Expected time: 5-10 minutes)")
    print()
    print("6. Download 3 files at the end:")
    print("   - pronunciation_scorer.pth")
    print("   - model_info.json")
    print("   - scaler_params.json")
    print()
    
    input("Press Enter when you've downloaded the model files...")
    
    # Step 4: Deploy model
    print_step(4, "Deploy Model to Backend")
    
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    print(f"Copy the 3 downloaded files to: {models_dir.absolute()}")
    print()
    print("Files needed:")
    print("  - pronunciation_scorer.pth")
    print("  - model_info.json")
    print("  - scaler_params.json")
    print()
    
    input("Press Enter when files are copied...")
    
    if not check_model_files():
        print("\n❌ Model files not found. Please copy them to backend/models/")
        sys.exit(1)
    
    # Step 5: Test deployment
    print_step(5, "Test ML Model")
    
    if test_ml_model():
        print()
        print("=" * 70)
        print("  ✅ SUCCESS! ML Model Deployed and Ready")
        print("=" * 70)
        print()
        print("📊 Your model is now active!")
        print()
        print("Test it:")
        print("  python test_analysis.py path/to/audio.wav wordname")
        print()
        print("Or start the backend:")
        print("  python main.py")
        print()
        print("API responses will now include:")
        print('  "scoring_method": "ml_model"')
        print()
    else:
        print()
        print("❌ Model deployment failed. Check error messages above.")
        print()
        print("Troubleshooting:")
        print("  1. Ensure all 3 files are in backend/models/")
        print("  2. Check file permissions")
        print("  3. Verify PyTorch is installed: pip install torch")
        print()
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
