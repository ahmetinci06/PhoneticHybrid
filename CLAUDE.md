# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PhoneticHybrid is a production-ready Turkish pronunciation analysis platform combining **Whisper (OpenAI open-source)** with **Phonemizer** for academic phoneme-level pronunciation assessment. It's a full-stack application where participants record Turkish words and receive detailed phoneme-level pronunciation feedback based on acoustic features.

## Architecture

### Two-Part System
- **Frontend**: React 18 + TypeScript + Material UI v6 (Vite)
- **Backend**: FastAPI (Python 3.10+) + Whisper + Phonemizer

### Analysis Pipeline
The system uses a hybrid approach combining:
1. **Whisper Speech Recognition** (local, open-source) - Turkish speech-to-text with no API costs
2. **Phonemizer** (eSpeak-NG backend) - Ground-truth phoneme generation
3. **Acoustic Analysis** (librosa + Praat) - Feature extraction (MFCCs, pitch, formants)
4. **Phoneme Alignment & Scoring** - Per-phoneme pronunciation quality assessment

**Key Benefits:**
- **No API costs** - Whisper runs completely locally
- **Privacy-first** - Audio never leaves your machine
- **No credentials needed** - No API keys or configuration required
- **Excellent Turkish support** - Whisper has strong multilingual capabilities

**Important**: The old ML training approach has been deprecated and moved to `backend/deprecated/`. The previous Azure Speech Services integration was replaced with Whisper (see `MIGRATION_TO_WHISPER.md` for migration details).

## Development Commands

### Quick Start (Recommended)

**Automated Setup:**
```bash
# macOS
./scripts/setup/setup-macos.sh

# Linux
./scripts/setup/setup-linux.sh

# Windows
scripts\setup\setup-windows.bat
```

**Start Development Servers:**
```bash
# macOS
./scripts/start/start-macos.sh

# Linux
./scripts/start/start-linux.sh

# Windows
scripts\start\start-windows.bat
```

### Manual Commands

**Backend - Start Development Server:**
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python main.py
# Runs on http://localhost:8000
# API docs at http://localhost:8000/docs
```

**Backend - Run with Uvicorn (production-like):**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Backend - Tests:**
```bash
cd backend
source venv/bin/activate
pytest
# Note: Limited test coverage currently exists
```

**Backend - Manual Setup:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Frontend - Start Development Server:**
```bash
cd frontend
npm run dev
# Runs on http://localhost:5173 (Vite default) or http://localhost:3000
```

**Frontend - Build for Production:**
```bash
cd frontend
npm run build
# Output to frontend/dist/
```

**Frontend - Lint:**
```bash
cd frontend
npm run lint
```

**Frontend - Manual Setup:**
```bash
cd frontend
npm install
```

## Key Configuration Files

### Backend Environment (.env)
Create `backend/.env` from `backend/.env.example` (optional):
```bash
# Backend server configuration
HOST=0.0.0.0
PORT=8000
DATA_DIR=../data

# Speech Recognition uses Whisper (OpenAI open-source)
# No API keys required - runs completely locally
# Whisper models download automatically on first use (~150MB for base model)
```

**No API credentials needed!** Whisper runs entirely on your local machine.

## Core Modules

### Backend Structure
- **`main.py`** - FastAPI app, API endpoints, CORS configuration
- **`inference.py`** - Pronunciation analysis engine (PronunciationAnalyzer class, Whisper integration)
- **`phoneme_service.py`** - Phoneme generation API (eSpeak-NG integration)
- **`review_api.py`** - Manual review interface for evaluators
- **`deprecated/`** - Old ML training code and Azure integration (archived)

### Frontend Structure
- **`src/App.tsx`** - Main app with routing
- **`src/components/`**:
  - `Welcome.tsx` - Welcome screen
  - `ConsentForm.tsx` - KVKK consent + participant registration
  - `OrthodonticSurvey.tsx` - 8-question Likert scale survey
  - `PronunciationTest.tsx` - Main recording interface (30 Turkish words)
  - `FinishScreen.tsx` - Completion screen
  - `PhonemePreview.tsx` - IPA phoneme visualization
- **`src/pages/ReviewPage.tsx`** - Manual review interface

## Key API Endpoints

### Production Pronunciation Analysis
**POST `/analyze`** - Main analysis endpoint (Whisper + Phoneme hybrid)
- Accepts: `.wav` file + `word` (form-data)
- Returns: Whisper recognition, phoneme sequence, per-phoneme scores, overall grade
- Whisper model downloads automatically on first use (~150MB base model)

**Example:**
```bash
curl -X POST http://localhost:8000/analyze \
  -F "file=@recording.wav" \
  -F "word=pencere"
```

**Response:**
```json
{
  "word": "pencere",
  "recognized_text": "pencere",
  "recognition_confidence": 0.91,
  "phonemes_target": "p e n d͡ʒ e ɾ e",
  "segment_scores": { "p": 0.96, "e": 0.91, "n": 0.90 },
  "overall": 0.88,
  "grade": "B (İyi)",
  "analysis_method": "whisper_hybrid"
}
```

### Phoneme Service
- **POST `/phoneme/generate`** - Generate IPA phonemes for a word
- **POST `/phoneme/analyze`** - Detailed phoneme analysis
- **GET `/phoneme/health`** - Check eSpeak-NG availability

### Data Collection
- **POST `/register`** - Register new participant (creates UUID)
- **POST `/survey`** - Save survey responses
- **POST `/upload`** - Upload audio recording (saves to `data/participant_xxx/kelimeler/`)

### Review Interface
- **GET `/review/participants`** - List all participants
- **GET `/review/recordings/{participant_id}`** - Get participant recordings
- **POST `/review/label`** - Save manual pronunciation scores
- **GET `/audio/{participant_id}/{filename}`** - Serve audio files

## Technical Implementation Details

### Acoustic Feature Extraction (`inference.py`)
The `PronunciationAnalyzer.extract_acoustic_features()` method extracts:
- **MFCCs**: 13 coefficients (spectral envelope)
- **Pitch (F0)**: Using librosa's PYIN algorithm (65-2093 Hz range)
- **Formants (F1, F2, F3)**: Via Praat/Parselmouth for phonetic accuracy
- **Energy**: RMS (root mean square)
- **Spectral features**: Centroid, rolloff, zero-crossing rate

### Phoneme Generation
- Uses Phonemizer library with eSpeak-NG backend
- Language: Turkish (`tr`)
- Platform-specific: Windows looks for `C:\Program Files\eSpeak NG\espeak-ng.exe`
- Linux/Mac: Uses `espeak-ng` from PATH

### Data Storage
Participant data stored in: `data/participant_{uuid}/`
```
data/
└── participant_xxx/
    ├── info.json          # Registration info
    ├── survey.json        # Likert scale responses
    └── kelimeler/         # Audio recordings
        ├── 00_araba.wav
        ├── 01_bahçe.wav
        └── ...
```

### Turkish Word List
30 words defined in `frontend/src/components/PronunciationTest.tsx`:
```typescript
const turkishWords = [
  'araba', 'bahçe', 'çiçek', 'diş', 'elma',
  // ... add/edit as needed
]
```

## Common Development Tasks

### Adding New Turkish Words
Edit `frontend/src/components/PronunciationTest.tsx`:
```typescript
const turkishWords = [
  'araba', 'bahçe', 'yeni_kelime', // Add here
]
```

### Customizing Acoustic Analysis
Modify `backend/inference.py`:
- `extract_acoustic_features()` - Add new features
- `turkish_vowel_formants` - Update formant reference values
- Scoring algorithms in `analyze_pronunciation_whisper()`

### Changing Phoneme Generation Settings
Edit `backend/phoneme_service.py` or `backend/inference.py`:
```python
from phonemizer import phonemize
phonemes = phonemize(
    word,
    language='tr',
    backend='espeak',
    with_stress=True  # Toggle stress markers
)
```

### CORS Configuration
Update `backend/main.py` if frontend URL changes:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    # Add new origins here
)
```

## Documentation

Comprehensive documentation in `docs/` folder:
- **Setup**: `docs/setup/QUICK_START.md`, `docs/setup/SETUP_GUIDE.md`
- **Migration**: `MIGRATION_TO_WHISPER.md` (Azure → Whisper migration guide)
- **API Reference**: `docs/guides/PRONUNCIATION_ANALYSIS_GUIDE.md`, `docs/guides/PHONEME_FEATURE.md`
- **Architecture**: `docs/architecture/SYSTEM_OVERVIEW.md`, `docs/architecture/PROJECT_STRUCTURE.md`
- **Deprecated**: `docs/deprecated/` (old ML training), `docs/azure/` (replaced by Whisper)

Interactive API docs available at http://localhost:8000/docs when backend is running.

## Important Notes

### Deprecated Features
- **Azure Speech Services integration** - Replaced with Whisper (see `MIGRATION_TO_WHISPER.md`)
- ML training workflow moved to `backend/deprecated/` and `ml_colab/`
- Old analysis endpoint `/analyze/audio` is deprecated - use `/analyze` instead
- POST `/upload` no longer performs analysis (backward compatibility only)

### eSpeak-NG Requirement
The phoneme service requires eSpeak-NG installation:
- **Windows**: Install from https://github.com/espeak-ng/espeak-ng/releases
- **Linux**: `sudo apt-get install espeak-ng`
- **Mac**: `brew install espeak-ng`

### Data Privacy (KVKK Compliance)
- All participants anonymized with UUID
- Consent explicitly required before data collection
- Audio stored locally, not shared externally
- Data used only for research purposes

### Whisper Speech Recognition
- **No API keys required** - Runs completely locally on your machine
- **Privacy-first** - Audio data never leaves your computer
- **No costs** - Free and open-source (OpenAI)
- **Excellent Turkish support** - Pre-trained multilingual model
- **Auto-download** - Base model (~150MB) downloads automatically on first use
- **First-time setup**: The first API call will take longer (1-2 minutes) while Whisper downloads the model
- Models stored in: `~/.cache/whisper/` (Linux/Mac) or `%USERPROFILE%\.cache\whisper\` (Windows)
- For migration from Azure, see `MIGRATION_TO_WHISPER.md`

### Performance Notes
- **First analysis**: 1-2 minutes (model download)
- **Subsequent analyses**: 2-5 seconds per recording (depending on hardware)
- **GPU acceleration**: Whisper automatically uses CUDA if available (significantly faster)
- **CPU-only**: Works fine on CPU, just slightly slower

## Technology Stack Summary

**Frontend:**
- React 18 + TypeScript
- Material UI v6 (@mui/material)
- Vite (build tool)
- axios (HTTP client)
- react-router-dom (routing)

**Backend:**
- FastAPI
- Whisper (OpenAI open-source speech recognition)
- Phonemizer (eSpeak-NG)
- librosa (audio processing)
- praat-parselmouth (phonetic analysis)
- scipy (phoneme alignment)
- PyTorch (required by Whisper, also for legacy ML support)
