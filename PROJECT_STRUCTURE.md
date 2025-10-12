# Project Structure

Complete directory tree of the PhoneticHybrid system.

```
phoneizer/
│
├── 📄 README.md                      # Main project documentation
├── 📄 SETUP_GUIDE.md                 # Installation & setup instructions
├── 📄 DEPLOYMENT.md                  # Production deployment guide
├── 📄 CONTRIBUTING.md                # Contribution guidelines
├── 📄 LICENSE                        # MIT License
├── 📄 PROJECT_STRUCTURE.md           # This file
├── 📄 .gitignore                     # Git ignore patterns
├── 🚀 start_dev.bat                  # Windows dev server launcher
├── 🚀 start_dev.sh                   # macOS/Linux dev server launcher
│
├── 📁 frontend/                      # React + MUI Application
│   ├── 📄 package.json               # Node dependencies
│   ├── 📄 tsconfig.json              # TypeScript config
│   ├── 📄 tsconfig.node.json         # Node-specific TS config
│   ├── 📄 vite.config.ts             # Vite bundler config
│   ├── 📄 index.html                 # HTML entry point
│   ├── 📄 README.md                  # Frontend documentation
│   │
│   └── 📁 src/
│       ├── 📄 main.tsx               # App entry + theme setup
│       ├── 📄 App.tsx                # Main app component & routing
│       ├── 📄 vite-env.d.ts          # Vite type definitions
│       │
│       └── 📁 components/
│           ├── 📄 Welcome.tsx        # Landing/welcome screen
│           ├── 📄 ConsentForm.tsx    # KVKK & personal info form
│           ├── 📄 LikertScale.tsx    # Reusable survey component
│           ├── 📄 OrthodonticSurvey.tsx  # Survey flow
│           ├── 📄 PronunciationTest.tsx  # Audio recording interface
│           └── 📄 FinishScreen.tsx   # Completion screen
│
├── 📁 backend/                       # FastAPI Server
│   ├── 📄 main.py                    # API endpoints + ML inference
│   ├── 📄 requirements.txt           # Python dependencies
│   ├── 📄 .env.example               # Environment variables template
│   └── 📄 README.md                  # Backend documentation
│
├── 📁 ml_colab/                      # Google Colab Training
│   ├── 📓 training_notebook.ipynb    # Complete training pipeline
│   ├── 📄 training_environment_setup.txt      # Colab setup guide
│   └── 📄 ai_training_instructions.txt        # Detailed training steps
│
├── 📁 models/                        # Trained ML Models
│   ├── 📄 .gitkeep                   # Keep directory in Git
│   └── 🤖 trained_model.pt           # Trained PyTorch model (after training)
│
└── 📁 data/                          # Participant Data
    ├── 📄 .gitkeep                   # Keep directory in Git
    │
    └── 📁 participant_{uuid}/        # Per-participant folder
        ├── 📄 info.json              # Personal information
        ├── 📄 survey.json            # Survey responses
        │
        └── 📁 kelimeler/             # Audio recordings
            ├── 🎵 00_araba.wav
            ├── 🎵 01_bahçe.wav
            ├── 🎵 02_çocuk.wav
            ├── 📄 00_araba_result.json
            ├── 📄 01_bahçe_result.json
            └── ...
```

## File Descriptions

### Root Level

| File | Purpose |
|------|---------|
| `README.md` | Project overview, architecture, quick start |
| `SETUP_GUIDE.md` | Detailed installation instructions |
| `DEPLOYMENT.md` | Production deployment strategies |
| `CONTRIBUTING.md` | Guidelines for contributors |
| `LICENSE` | MIT License text |
| `.gitignore` | Files to exclude from Git |
| `start_dev.bat` | Windows script to launch dev servers |
| `start_dev.sh` | Unix script to launch dev servers |

### Frontend Structure

```
frontend/
├── Configuration Files
│   ├── package.json          # Dependencies: React, MUI, TypeScript
│   ├── tsconfig.json         # TypeScript compiler settings
│   ├── vite.config.ts        # Vite build tool + proxy config
│   └── index.html            # HTML shell
│
├── Source Code
│   ├── main.tsx              # App initialization + MUI theme
│   └── App.tsx               # Route management & state
│
└── Components (src/components/)
    ├── Welcome.tsx           # Hero section with "Start" button
    ├── ConsentForm.tsx       # KVKK consent + personal data collection
    ├── LikertScale.tsx       # 5-point scale survey widget
    ├── OrthodonticSurvey.tsx # 8-question survey interface
    ├── PronunciationTest.tsx # Core recording logic (MediaRecorder API)
    └── FinishScreen.tsx      # Thank you page with restart option
```

### Backend Structure

```
backend/
├── main.py                   # FastAPI app with 5 endpoints:
│                             #   - GET  / (health)
│                             #   - POST /register
│                             #   - POST /survey
│                             #   - POST /upload
│                             #   - GET  /health
│
├── requirements.txt          # Python packages:
│                             #   - fastapi, uvicorn
│                             #   - torch, librosa
│                             #   - praat-parselmouth
│                             #   - phonemizer
│
└── .env.example              # Configuration template
```

### ML Training Structure

```
ml_colab/
├── training_notebook.ipynb   # Jupyter notebook with:
│                             #   - Data loading from Drive
│                             #   - Feature extraction (37 features)
│                             #   - Model training (PyTorch)
│                             #   - Evaluation & export
│
├── training_environment_setup.txt    # Colab environment guide:
│                                    #   - Dependencies
│                                    #   - GPU setup
│                                    #   - Troubleshooting
│
└── ai_training_instructions.txt      # Step-by-step training:
                                      #   - Pre-training checklist
                                      #   - Training workflow
                                      #   - Hyperparameter tuning
```

### Data Structure

```
data/
└── participant_{uuid}/
    ├── info.json             # {name, age, gender, consent, timestamp}
    ├── survey.json           # {responses: [1-5, ...], timestamp}
    │
    └── kelimeler/
        ├── 00_araba.wav      # Audio recording (16kHz WAV)
        ├── 00_araba_result.json  # {word, score, confidence, feedback}
        ├── 01_bahçe.wav
        ├── 01_bahçe_result.json
        └── ...
```

## Data Flow

```
┌─────────────┐
│   Browser   │
│  (Frontend) │
└──────┬──────┘
       │ 1. User fills form
       │ 2. Records audio
       │ 3. Sends POST /upload
       ▼
┌─────────────┐
│   FastAPI   │
│  (Backend)  │
└──────┬──────┘
       │ 4. Saves to /data
       │ 5. Loads audio
       │ 6. Extracts features (37D)
       ▼
┌─────────────┐
│  ML Model   │
│  (PyTorch)  │
└──────┬──────┘
       │ 7. Inference
       │ 8. Returns score
       ▼
┌─────────────┐
│   Backend   │
│  (FastAPI)  │
└──────┬──────┘
       │ 9. Saves result.json
       │ 10. Returns to frontend
       ▼
┌─────────────┐
│   Browser   │
│  (Display)  │
└─────────────┘
```

## Component Dependencies

### Frontend Dependencies
```
React 18
├── @mui/material (UI components)
├── @emotion/react (CSS-in-JS)
└── react-router-dom (routing)
```

### Backend Dependencies
```
FastAPI
├── uvicorn (ASGI server)
├── PyTorch (ML inference)
├── librosa (audio processing)
├── praat-parselmouth (phonetic analysis)
└── phonemizer (IPA transcription)
```

## Key Features by File

### Frontend

| Component | Features |
|-----------|----------|
| `Welcome.tsx` | Hero section, gradient title, start button |
| `ConsentForm.tsx` | Validation, KVKK text, API integration |
| `LikertScale.tsx` | 5-point scale, hover effects, accessibility |
| `OrthodonticSurvey.tsx` | Progress bar, validation, 8 questions |
| `PronunciationTest.tsx` | MediaRecorder, upload, real-time feedback |
| `FinishScreen.tsx` | Completion message, restart functionality |

### Backend

| Function | Purpose |
|----------|---------|
| `register_participant()` | Create UUID, save info.json |
| `save_survey()` | Validate & save survey.json |
| `upload_audio()` | Save WAV, extract features, run inference |
| `extract_features()` | 13 MFCCs + spectral + formants + F0 |
| `analyze_pronunciation()` | ML inference, score generation |

## File Sizes (Approximate)

| File/Directory | Size |
|----------------|------|
| `frontend/node_modules/` | ~200 MB |
| `backend/venv/` | ~500 MB |
| `models/trained_model.pt` | ~1-2 MB |
| Source code total | ~500 KB |
| Per participant data | ~2-5 MB |

## Ports & URLs

| Service | Port | URL |
|---------|------|-----|
| Frontend Dev | 3000 | http://localhost:3000 |
| Backend API | 8000 | http://localhost:8000 |
| API Docs | 8000 | http://localhost:8000/docs |
| Redoc | 8000 | http://localhost:8000/redoc |

## Configuration Files

| File | Purpose |
|------|---------|
| `frontend/package.json` | Node dependencies, scripts |
| `frontend/tsconfig.json` | TypeScript compiler options |
| `frontend/vite.config.ts` | Dev server, proxy, build config |
| `backend/requirements.txt` | Python package versions |
| `backend/.env` | Environment variables (not in Git) |
| `.gitignore` | Exclude: node_modules, venv, data, models |

## Important Notes

1. **Git Ignored**: `node_modules/`, `venv/`, `data/`, `*.pt` files
2. **Required Before Training**: Collect participant data first
3. **Model File**: Must be copied from Colab to `models/` after training
4. **CORS**: Backend allows localhost:3000 and localhost:5173
5. **Audio Format**: WAV files, resampled to 16kHz for analysis
