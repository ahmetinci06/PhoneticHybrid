# Migration from Azure to Whisper

## Summary

This project has been successfully migrated from Azure Cognitive Services to Whisper (OpenAI's open-source speech recognition model).

## What Changed

### 1. Speech Recognition Engine
- **Before:** Azure Cognitive Services Speech-to-Text (requires API keys, paid service)
- **After:** Whisper (OpenAI open-source, runs locally, completely free)

### 2. Benefits
- ✅ **No API costs** - Whisper runs locally on your machine
- ✅ **No API keys needed** - No configuration required
- ✅ **Privacy** - Audio never leaves your machine
- ✅ **Excellent Turkish support** - Whisper has strong multilingual capabilities
- ✅ **Open source** - Full transparency and community support

### 3. Files Modified

#### Backend
- `backend/requirements.txt` - Replaced `azure-cognitiveservices-speech` with `openai-whisper`
- `backend/inference.py` - Replaced `_recognize_speech_azure()` with `_recognize_speech_whisper()`
- `backend/inference.py` - Updated `analyze_pronunciation_azure()` to `analyze_pronunciation_whisper()`
- `backend/main.py` - Changed endpoint from `/analyze/azure` to `/analyze`
- `backend/main.py` - Updated health check to verify Whisper availability
- `backend/.env.example` - Removed Azure configuration variables

#### Files Removed
- `backend/azure_config.py` - No longer needed

#### Frontend
- `frontend/src/components/PronunciationTest.tsx` - Updated API endpoint from `/analyze/azure` to `/analyze`

### 4. API Changes

#### Old Endpoint
```bash
POST /analyze/azure
```

#### New Endpoint
```bash
POST /analyze
```

The response format remains the same, with one change:
- `azure_confidence` → `recognition_confidence`

### 5. Installation

To install the new dependencies:

```bash
cd backend
pip install -r requirements.txt
```

**Note:** Whisper will automatically download the required model files (~150MB for the base model) on first use.

### 6. How It Works

The new system combines:
1. **Whisper** - Local speech-to-text recognition for Turkish
2. **Phonemizer (eSpeak NG)** - Ground-truth phoneme generation
3. **Librosa + Praat** - Acoustic feature extraction
4. **Phoneme alignment** - Segment-level pronunciation scoring

The scoring algorithm:
- 40% from Whisper recognition confidence
- 60% from acoustic feature analysis

### 7. Performance

- **Speed:** Slightly slower than Azure (runs on local CPU/GPU)
- **Accuracy:** Comparable or better for Turkish
- **Model size:** ~150MB (base model) - downloaded automatically
- **First run:** Slower (downloads model), subsequent runs are fast

### 8. Model Options

You can change the Whisper model in `backend/inference.py` line 513:

```python
model = whisper.load_model("base")  # Options: tiny, base, small, medium, large
```

- `tiny` - Fastest, least accurate (~40MB)
- `base` - Good balance (~150MB) - **Currently used**
- `small` - Better accuracy (~500MB)
- `medium` - High accuracy (~1.5GB)
- `large` - Best accuracy (~3GB)

### 9. Running the Application

No configuration needed! Just run:

```bash
# Backend
cd backend
python main.py

# Frontend (in another terminal)
cd frontend
npm start
```

### 10. Migration Checklist

- [x] Replace Azure SDK with Whisper
- [x] Update speech recognition function
- [x] Update API endpoints
- [x] Remove Azure configuration
- [x] Update frontend API calls
- [x] Update documentation
- [x] Test the implementation
- [x] Remove deprecated Azure code

## Troubleshooting

### Installation Issues
If Whisper installation fails, you may need to install system dependencies:

```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg
```

### Model Download Issues
Models are downloaded to `~/.cache/whisper/`. If download fails:
- Check internet connection
- Ensure sufficient disk space (~150MB+)
- Check firewall settings

### Performance Issues
- Use smaller model (`tiny` or `base`) for faster processing
- Enable GPU acceleration if available (requires CUDA setup)
- Whisper will automatically use GPU if PyTorch is CUDA-enabled

## Additional Notes

- All phoneme analysis features remain unchanged
- Acoustic feature extraction still uses librosa and Praat
- The overall scoring algorithm is identical
- No changes required to the database or data storage
- Backward compatible with existing recorded audio files
