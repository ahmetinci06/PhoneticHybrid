# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PhoneticHybrid is a production-ready Turkish pronunciation analysis platform combining **Azure Speech Services** with **Phonemizer** for academic phoneme-level pronunciation assessment. It's a full-stack application where participants record Turkish words and receive detailed phoneme-level pronunciation feedback based on acoustic features.

## Architecture

### Two-Part System
- **Frontend**: React 18 + TypeScript + Material UI v6 (Vite)
- **Backend**: FastAPI (Python 3.10+) + Azure Cognitive Services

### Analysis Pipeline
The system uses a hybrid approach combining:
1. **Azure Speech-to-Text** (tr-TR) - Production speech recognition
2. **Phonemizer** (eSpeak-NG backend) - Ground-truth phoneme generation
3. **Acoustic Analysis** (librosa + Praat) - Feature extraction (MFCCs, pitch, formants)
4. **Phoneme Alignment & Scoring** - Per-phoneme pronunciation quality assessment

**Important**: The old ML training approach has been deprecated and moved to `backend/deprecated/`. The current system uses Azure's pre-trained models instead.

## Development Commands

### Backend

**Start Development Server:**
```bash
cd backend
python main.py
# Runs on http://localhost:8000
# API docs at http://localhost:8000/docs
```

**Run with Uvicorn (production-like):**
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Tests:**
```bash
cd backend
pytest
# Note: Limited test coverage currently exists
```

**Setup:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend

**Start Development Server:**
```bash
cd frontend
npm run dev
# Runs on http://localhost:5173 (Vite default) or http://localhost:3000
```

**Build for Production:**
```bash
cd frontend
npm run build
# Output to frontend/dist/
```

**Lint:**
```bash
cd frontend
npm run lint
```

**Setup:**
```bash
cd frontend
npm install
```

## Key Configuration Files

### Backend Environment (.env)
Create `backend/.env` from `backend/.env.example`:
```bash
# Required for Azure integration
AZURE_SPEECH_KEY=your_azure_speech_key_here
AZURE_REGION=your_azure_region_here  # e.g., eastus, westeurope

# Optional
HOST=0.0.0.0
PORT=8000
DATA_DIR=../data
```

**Get Azure credentials:**
1. Create Azure account: https://portal.azure.com
2. Create a "Speech" resource
3. Copy Key and Region from resource page

## Core Modules

### Backend Structure
- **`main.py`** - FastAPI app, API endpoints, CORS configuration
- **`inference.py`** - Pronunciation analysis engine (PronunciationAnalyzer class)
- **`azure_config.py`** - Azure Speech Services configuration
- **`phoneme_service.py`** - Phoneme generation API (eSpeak-NG integration)
- **`review_api.py`** - Manual review interface for evaluators
- **`deprecated/`** - Old ML training code (archived)

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
**POST `/analyze/azure`** - Main analysis endpoint (Azure + Phoneme hybrid)
- Accepts: `.wav` file + `word` (form-data)
- Returns: Azure recognition, phoneme sequence, per-phoneme scores, overall grade

**Example:**
```bash
curl -X POST http://localhost:8000/analyze/azure \
  -F "file=@recording.wav" \
  -F "word=pencere"
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
- Scoring algorithms in `analyze_pronunciation_azure()`

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
- **Azure**: `docs/azure/AZURE_INTEGRATION_SUMMARY.md`
- **API Reference**: `docs/guides/PRONUNCIATION_ANALYSIS_GUIDE.md`, `docs/guides/PHONEME_FEATURE.md`
- **Architecture**: `docs/architecture/SYSTEM_OVERVIEW.md`, `docs/architecture/PROJECT_STRUCTURE.md`
- **Deprecated**: `docs/deprecated/` (old ML training approach)

Interactive API docs available at http://localhost:8000/docs when backend is running.

## Important Notes

### Deprecated Features
- ML training workflow moved to `backend/deprecated/` and `ml_colab/`
- Old analysis endpoint `/analyze/audio` is deprecated - use `/analyze/azure` instead
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

### Azure Speech Services
- Required for production pronunciation analysis
- Pre-trained models eliminate need for custom ML training
- Turkish language model: `tr-TR`
- See `docs/azure/AZURE_INTEGRATION_SUMMARY.md` for setup

## Technology Stack Summary

**Frontend:**
- React 18 + TypeScript
- Material UI v6 (@mui/material)
- Vite (build tool)
- axios (HTTP client)
- react-router-dom (routing)

**Backend:**
- FastAPI
- Azure Cognitive Services Speech SDK
- Phonemizer (eSpeak-NG)
- librosa (audio processing)
- praat-parselmouth (phonetic analysis)
- scipy (phoneme alignment)
- PyTorch (optional, for legacy ML support)
