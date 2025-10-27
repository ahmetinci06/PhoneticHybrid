# PhoneticHybrid - Visual Guide 🎨

## System Architecture Diagram

```
╔═══════════════════════════════════════════════════════════════════════╗
║                    PHONETICHYBRID SYSTEM ARCHITECTURE                  ║
╚═══════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────┐
│                         USER EXPERIENCE FLOW                             │
└─────────────────────────────────────────────────────────────────────────┘

    👤 Participant
       │
       │ Opens Browser
       ▼
┌──────────────────┐
│   Welcome.tsx    │  "PhoneticHybrid - Başlamak İçin Tıklayın"
│   (Screen 1)     │
└────────┬─────────┘
         │ Click Start
         ▼
┌──────────────────┐
│ ConsentForm.tsx  │  Name, Age, Gender, KVKK Consent
│   (Screen 2)     │  → POST /register → participant_id
└────────┬─────────┘
         │ Submit
         ▼
┌──────────────────┐
│OrthodonticSur    │  8 Questions, Likert Scale (1-5)
│   vey.tsx        │  → POST /survey
│   (Screen 3)     │
└────────┬─────────┘
         │ Complete
         ▼
┌──────────────────┐
│Pronunciation     │  Record 30 Words
│   Test.tsx       │  For each word:
│   (Screen 4)     │    - Display word
└────────┬─────────┘    - Record audio (MediaRecorder)
         │              - Upload → POST /upload
         │              - Get score & feedback
         │              - Next word
         ▼
┌──────────────────┐
│ FinishScreen.tsx │  "Tebrikler! Testi Başarıyla Tamamladınız"
│   (Screen 5)     │
└──────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                         BACKEND PROCESSING                               │
└─────────────────────────────────────────────────────────────────────────┘

   Frontend                Backend                   ML Pipeline
       │                       │                           │
       │ POST /upload          │                           │
       ├──────────────────────►│                           │
       │ (audio + metadata)    │                           │
       │                       │                           │
       │                       │ 1. Save to disk           │
       │                       │    /data/participant_x/   │
       │                       │    kelimeler/word.wav     │
       │                       │                           │
       │                       │ 2. Load audio             │
       │                       │    librosa.load()         │
       │                       │    → numpy array          │
       │                       │                           │
       │                       │ 3. Extract features       │
       │                       ├──────────────────────────►│
       │                       │                           │
       │                       │              ┌────────────┴──────────┐
       │                       │              │ Feature Extraction     │
       │                       │              │ ─────────────────────  │
       │                       │              │ • MFCCs (13×2)         │
       │                       │              │ • Spectral (3)         │
       │                       │              │ • ZCR, RMS (2)         │
       │                       │              │ • Formants (3)         │
       │                       │              │ • F0 stats (2)         │
       │                       │              │ • Duration (1)         │
       │                       │              │ ─────────────────────  │
       │                       │              │ Total: 37 features     │
       │                       │              └────────────┬──────────┘
       │                       │                           │
       │                       │ 4. ML Inference           │
       │                       │◄──────────────────────────┤
       │                       │    (37D vector)           │
       │                       │                           │
       │                       │              ┌────────────▼──────────┐
       │                       │              │ PyTorch Model          │
       │                       │              │ ──────────────────────│
       │                       │              │ Input: [37]            │
       │                       │              │ Dense: [128] + ReLU    │
       │                       │              │ Dense: [64]  + ReLU    │
       │                       │              │ Dense: [32]  + ReLU    │
       │                       │              │ Output: [1]  → Sigmoid │
       │                       │              │ ──────────────────────│
       │                       │              │ Score: 0.0 - 1.0       │
       │                       │              └────────────┬──────────┘
       │                       │                           │
       │                       │ 5. Generate feedback      │
       │                       │◄──────────────────────────┤
       │                       │                           │
       │                       │ 6. Save result.json       │
       │                       │    {word, score, feedback}│
       │                       │                           │
       │ 7. Return JSON        │                           │
       │◄──────────────────────┤                           │
       │ {score, feedback}     │                           │
       ▼                       │                           │
   Display Result             │                           │


┌─────────────────────────────────────────────────────────────────────────┐
│                      ML TRAINING WORKFLOW (Colab)                        │
└─────────────────────────────────────────────────────────────────────────┘

┌───────────────┐
│ Google Drive  │  /phoneizer/data/
│ (Data Upload) │  ├── participant_001/
└───────┬───────┘  ├── participant_002/
        │          └── ...
        │
        ▼
┌───────────────────────────────────────────────────────────────┐
│  Google Colab (training_notebook.ipynb)                       │
│  ─────────────────────────────────────────────────────────── │
│                                                                │
│  1. Mount Drive                                                │
│     from google.colab import drive                            │
│     drive.mount('/content/drive')                             │
│                                                                │
│  2. Load Data                                                  │
│     for each participant:                                     │
│       - Read info.json                                        │
│       - Load audio files                                      │
│       - Create DataFrame                                      │
│                                                                │
│  3. Feature Extraction                                         │
│     for each audio file:                                      │
│       - Extract 37 features                                   │
│       - Store in feature matrix X                             │
│                                                                │
│  4. Label Assignment                                           │
│     ⚠️  REPLACE WITH REAL LABELS!                             │
│                                                                │
│  5. Train/Test Split                                           │
│     X_train, X_test, y_train, y_test                          │
│     80% train, 20% test                                       │
│                                                                │
│  6. Model Training                                             │
│     for epoch in range(50):                                   │
│       - Forward pass                                          │
│       - Compute loss                                          │
│       - Backward pass                                         │
│       - Update weights                                        │
│       - Validate                                              │
│                                                                │
│  7. Save Model                                                 │
│     torch.save(model, 'trained_model.pt')                     │
│     → Download to local                                       │
│                                                                │
└────────────────────────────────┬──────────────────────────────┘
                                 │
                                 ▼
                        ┌────────────────┐
                        │ trained_model  │
                        │     .pt        │
                        │ (~1-2 MB)      │
                        └────────┬───────┘
                                 │
                                 │ Copy to local
                                 ▼
                        ┌────────────────┐
                        │ /models/       │
                        │ trained_model  │
                        │     .pt        │
                        └────────────────┘
                                 │
                                 │ Load on backend start
                                 ▼
                        ┌────────────────┐
                        │ Backend uses   │
                        │ for inference  │
                        └────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                          DATA STORAGE LAYOUT                             │
└─────────────────────────────────────────────────────────────────────────┘

phoneizer/
│
├── data/
│   │
│   ├── participant_<uuid-1>/
│   │   ├── info.json ─────────────────┐
│   │   │   {                          │
│   │   │     "id": "uuid-1",          │ Participant
│   │   │     "name": "Ali Yılmaz",    │ Metadata
│   │   │     "age": 25,               │
│   │   │     "gender": "Erkek",       │
│   │   │     "consent": true          │
│   │   │   }                          │
│   │   │                              │
│   │   ├── survey.json ───────────────┤
│   │   │   {                          │
│   │   │     "responses": [           │ Survey
│   │   │       5, 4, 3, 5, 4,         │ Responses
│   │   │       5, 3, 4                │
│   │   │     ]                        │
│   │   │   }                          │
│   │   │                              │
│   │   └── kelimeler/ ────────────────┘
│   │       ├── 00_araba.wav ──┐
│   │       ├── 00_araba_result.json   │
│   │       │   {                      │ Audio
│   │       │     "word": "araba",     │ +
│   │       │     "score": 0.85,       │ Analysis
│   │       │     "feedback": "İyi!"   │ Results
│   │       │   }                      │
│   │       ├── 01_bahçe.wav          │
│   │       ├── 01_bahçe_result.json  │
│   │       └── ...                   ─┘
│   │
│   ├── participant_<uuid-2>/
│   │   └── ... (same structure)
│   │
│   └── participant_<uuid-N>/
│       └── ...


┌─────────────────────────────────────────────────────────────────────────┐
│                      TECHNOLOGY STACK LAYERS                             │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│  PRESENTATION LAYER                                                      │
│  ──────────────────────────────────────────────────────────────────────│
│  React 18 + TypeScript + Material UI v6                                │
│  • Modern component-based UI                                            │
│  • Responsive design (mobile + desktop)                                 │
│  • Real-time form validation                                            │
│  • MediaRecorder API for audio                                          │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ HTTP REST API
                                    │ JSON payloads
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  APPLICATION LAYER                                                       │
│  ──────────────────────────────────────────────────────────────────────│
│  FastAPI (Python 3.10+)                                                 │
│  • Async request handling                                               │
│  • Pydantic validation                                                  │
│  • CORS middleware                                                      │
│  • File upload handling                                                 │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ Function calls
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  PROCESSING LAYER                                                        │
│  ──────────────────────────────────────────────────────────────────────│
│  librosa + praat-parselmouth + phonemizer                               │
│  • Audio loading & resampling                                           │
│  • MFCC extraction                                                      │
│  • Formant analysis                                                     │
│  • Pitch tracking                                                       │
│  • Spectral feature computation                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ Feature vectors
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  INTELLIGENCE LAYER                                                      │
│  ──────────────────────────────────────────────────────────────────────│
│  PyTorch 2.1.2                                                          │
│  • Deep neural network                                                  │
│  • Forward propagation                                                  │
│  • Sigmoid activation                                                   │
│  • CPU/GPU inference                                                    │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ Predictions
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  PERSISTENCE LAYER                                                       │
│  ──────────────────────────────────────────────────────────────────────│
│  File System                                                            │
│  • JSON metadata (info, survey, results)                                │
│  • WAV audio files                                                      │
│  • PyTorch model files (.pt)                                            │
└─────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                        DEPLOYMENT TOPOLOGY                               │
└─────────────────────────────────────────────────────────────────────────┘

DEVELOPMENT:
┌──────────────────┐
│  localhost:3000  │  Frontend (Vite Dev Server)
└────────┬─────────┘
         │
         │ Proxy /api → localhost:8000
         ▼
┌──────────────────┐
│  localhost:8000  │  Backend (Uvicorn)
└────────┬─────────┘
         │
         │ Load model
         ▼
┌──────────────────┐
│  /models/*.pt    │  Trained Model
└──────────────────┘

PRODUCTION:
┌──────────────────┐
│  CDN / Vercel    │  Frontend (Static Build)
│  your-app.com    │
└────────┬─────────┘
         │
         │ HTTPS API calls
         ▼
┌──────────────────┐
│  Railway/Render  │  Backend (Containerized)
│  api.your.com    │
└────────┬─────────┘
         │
         ├────────► ┌──────────────┐
         │          │ PostgreSQL   │  Metadata (optional)
         │          └──────────────┘
         │
         ├────────► ┌──────────────┐
         │          │ S3 / MinIO   │  Audio Storage (optional)
         │          └──────────────┘
         │
         └────────► ┌──────────────┐
                    │ Redis Cache  │  Feature Cache (optional)
                    └──────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                      FEATURE EXTRACTION PIPELINE                         │
└─────────────────────────────────────────────────────────────────────────┘

Input: word.wav (audio file)
│
├─ librosa.load(sr=16000)
│  └─► numpy array (waveform)
│
├─ MFCCs (librosa.feature.mfcc)
│  ├─► 13 coefficients
│  ├─► Mean → 13 features
│  └─► Std  → 13 features
│       Subtotal: 26 features
│
├─ Spectral Features
│  ├─► Centroid  (librosa.feature.spectral_centroid)
│  ├─► Rolloff   (librosa.feature.spectral_rolloff)
│  └─► Bandwidth (librosa.feature.spectral_bandwidth)
│       Subtotal: 3 features
│
├─ Temporal Features
│  └─► Zero Crossing Rate (librosa.feature.zero_crossing_rate)
│       Subtotal: 1 feature
│
├─ Energy
│  └─► RMS (librosa.feature.rms)
│       Subtotal: 1 feature
│
├─ Formants (Praat/Parselmouth)
│  ├─► F1 (first formant)
│  ├─► F2 (second formant)
│  └─► F3 (third formant)
│       Subtotal: 3 features
│
├─ Pitch (Praat/Parselmouth)
│  ├─► F0 mean
│  └─► F0 std
│       Subtotal: 2 features
│
└─ Duration
   └─► Audio length (seconds)
        Subtotal: 1 feature

Output: [37-dimensional feature vector]
        ↓
    ML Model Input
```

## Quick Reference

### Ports
- **3000** - Frontend
- **8000** - Backend

### Key Commands
```bash
# Start
start_dev.bat  # Windows
./start_dev.sh # Unix

# Backend
cd backend && python main.py

# Frontend
cd frontend && npm run dev
```

### File Locations
- Components: `frontend/src/components/`
- API: `backend/main.py`
- Training: `ml_colab/training_notebook.ipynb`
- Data: `data/participant_*/`
- Models: `models/trained_model.pt`

### API Endpoints
- `POST /register` - New participant
- `POST /survey` - Save survey
- `POST /upload` - Audio analysis
- `GET /health` - System status
- `GET /docs` - API documentation

---

*Visual guide for PhoneticHybrid system architecture*
