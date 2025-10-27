# Deprecated ML Training Code

This directory contains archived code from the previous ML training approach.

## Archived Files

The following files have been moved here as the project has migrated to using Azure Speech Services for pronunciation analysis:

### Python Scripts
- `train_ml_model.py` - Old custom model training workflow script
- `prepare_training_data.py` - Data preparation for model training
- `test_analysis.py` - Testing utilities for old model  
- `ml_scorer.py` - PyTorch-based pronunciation scorer (replaced by Azure)

### Training Materials
- `ml_colab/` - Google Colab notebooks
  - `training_notebook.ipynb` - Main training notebook
  - `pronunciation_scoring_training.ipynb` - Alternative training approach
  - `training_environment_setup.txt` - Setup instructions
  - `ai_training_instructions.txt` - Detailed training guide

### Documentation
- `reorganize_docs.bat` - Documentation reorganization script
- `reorganize_docs.sh` - Unix version of reorganization script  
- `REORGANIZATION_GUIDE.md` - Guide for documentation structure

## Why Deprecated?

The project has transitioned from local ML model training to a hybrid approach using:
- **Azure Cognitive Services Speech to Text** for speech recognition
- **Phonemizer (eSpeak NG)** for ground-truth phoneme sequences
- **Acoustic feature analysis** using librosa and Praat for detailed phoneme-level scoring

This new approach provides more accurate and production-ready pronunciation analysis without requiring local model training.

## Reference Only

These files are kept for archival and reference purposes only. They are no longer actively maintained or used in the application.
