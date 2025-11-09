# PhoneticHybrid 🎙️

A production-ready Turkish pronunciation analysis platform using **Whisper (OpenAI)** + **Phonemizer** for academic phoneme-level pronunciation assessment.

## 🎯 Overview

PhoneticHybrid is a full-stack web platform where participants:
1. Record Turkish words
2. Audio is analyzed using Whisper speech recognition (local, open-source)
3. Receive detailed phoneme-level pronunciation feedback
4. Get actionable insights based on acoustic features

**Perfect for:** Linguistic research, speech therapy, language learning applications, pronunciation assessment

**Key Features:**
- ✅ **Zero API costs** - Runs completely locally
- 🔒 **Privacy-first** - Audio never leaves your machine
- 🌐 **Open-source** - No API keys or credentials needed
- 🇹🇷 **Excellent Turkish support** - Pre-trained multilingual model

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────────────────┐
│              WHISPER-BASED ARCHITECTURE (LOCAL)                │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐ │
│  │   Frontend   │─────▶│   Backend    │─────▶│   Whisper    │ │
│  │ React + MUI  │◀─────│   FastAPI    │◀─────│  (Local AI)  │ │
│  └──────────────┘      └──────────────┘      └──────────────┘ │
│                               │                                  │
│                               ├─────▶ Phonemizer (eSpeak NG)    │
│                               ├─────▶ Acoustic Analysis         │
│                               │       (librosa, Praat)          │
│                               └─────▶ Phoneme Alignment         │
│                                                                  │
└────────────────────────────────────────────────────────────────┘
```

### Tech Stack

**Frontend:**
- React 18
- Material UI v6
- TypeScript
- Vite

**Backend:**
- FastAPI (Python 3.10+)
- Whisper (OpenAI open-source speech recognition)
- Phonemizer (eSpeak NG backend)
- librosa (audio processing)
- praat-parselmouth (phonetic analysis)
- scipy (phoneme alignment)

**Analysis Pipeline:**
- Whisper Speech-to-Text (local, multilingual)
- Ground-truth phoneme generation (Phonemizer)
- Acoustic feature extraction (MFCCs, formants, F0)
- Phoneme-level alignment and scoring

## 📁 Project Structure

```
phoneizer/
├── frontend/                # React + MUI application
│   ├── src/
│   │   ├── components/
│   │   │   ├── Welcome.tsx
│   │   │   ├── ConsentForm.tsx
│   │   │   ├── LikertScale.tsx
│   │   │   ├── OrthodonticSurvey.tsx
│   │   │   ├── PronunciationTest.tsx
│   │   │   └── FinishScreen.tsx
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── backend/                 # FastAPI server
│   ├── main.py             # API endpoints + ML inference
│   ├── requirements.txt
│   └── .env.example
│
├── ml_colab/               # Google Colab training
│   ├── training_notebook.ipynb
│   ├── training_environment_setup.txt
│   └── ai_training_instructions.txt
│
├── models/                 # Trained ML models
│   └── trained_model.pt   # (created after training)
│
├── data/                   # Participant data
│   └── participant_xxx/
│       ├── info.json
│       ├── survey.json
│       └── kelimeler/
│           └── *.wav
│
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.10+
- **eSpeak-NG** (for phoneme generation)

### Automated Setup (Recommended)

Choose your operating system and run the setup script:

**macOS:**
```bash
./scripts/setup/setup-macos.sh
```

**Linux:**
```bash
./scripts/setup/setup-linux.sh
```

**Windows:**
```cmd
scripts\setup\setup-windows.bat
```

The setup script will:
- ✅ Verify prerequisites (Python, Node.js, eSpeak-NG)
- ✅ Install eSpeak-NG if missing (macOS/Linux)
- ✅ Create Python virtual environment
- ✅ Install all Python dependencies
- ✅ Install all Node.js dependencies
- ✅ Create configuration files

### Start Development Servers

**macOS:**
```bash
./scripts/start/start-macos.sh
```

**Linux:**
```bash
./scripts/start/start-linux.sh
```

**Windows:**
```cmd
scripts\start\start-windows.bat
```

### Access Application

- **Frontend:** http://localhost:5173 (or http://localhost:3000)
- **Backend:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

**Note:** On first run, Whisper will download a ~150MB model (takes 1-2 minutes)

## 🎓 How It Works (Whisper-Based Approach)

### Analysis Pipeline

1. **Speech Recognition** (Whisper)
   - Audio processed locally by Whisper AI
   - Multilingual model with excellent Turkish support
   - Returns recognized text + confidence score
   - **Privacy-first:** Audio never leaves your machine

2. **Ground-Truth Phonemes** (Phonemizer)
   - Target word converted to IPA phonemes
   - Uses eSpeak NG Turkish backend
   - Produces expected pronunciation sequence

3. **Acoustic Feature Extraction**
   - MFCCs (13 coefficients)
   - Pitch (F0) analysis
   - Formants (F1, F2, F3) via Praat
   - Spectral features
   - Energy characteristics

4. **Phoneme-Level Scoring**
   - Align recognized text with target phonemes
   - Score each phoneme based on acoustic quality
   - Combine Whisper confidence with acoustic scores
   - Generate per-phoneme feedback

5. **Overall Assessment**
   - Weighted score: 40% Recognition + 60% Acoustic
   - Letter grade (A-F)
   - Detailed phoneme breakdown

### Migration from Old Approaches

The previous custom ML training workflow and Azure integration have been **deprecated** and moved to `/backend/deprecated/` and `/docs/deprecated/`. The new Whisper-based approach offers:

✅ **No training required** - Use Whisper's pre-trained models
✅ **Zero API costs** - Runs completely locally
✅ **Better privacy** - Audio never leaves your machine
✅ **No credentials needed** - No API keys to configure
✅ **Excellent accuracy** - Production-grade speech recognition
✅ **Easy deployment** - Just install and run

**Old files archived in:** `/backend/deprecated/`, `/docs/deprecated/`, and `/ml_colab/`

## 📊 User Flow

1. **Welcome Screen** - Intro and start button
2. **KVKK Consent Form** - Personal info + data consent
3. **Orthodontic Survey** - 8-question Likert scale
4. **Pronunciation Test** - Record 30 Turkish words
5. **Finish Screen** - Thank you + completion

## 🔧 API Endpoints

### Core Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/register` | Register new participant |
| POST | `/survey` | Save survey responses |
| POST | `/upload` | Upload audio + analyze |
| GET | `/health` | System status |

### Phoneme API
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/phoneme/generate` | Generate IPA phonemes for a word |
| POST | `/phoneme/analyze` | Detailed phoneme analysis |
| POST | `/phoneme/batch` | Process multiple words |
| GET | `/phoneme/health` | Check phoneme service status |

**See:** `PHONEME_FEATURE.md` for complete documentation

### Pronunciation Analysis API
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/analyze/audio` | Legacy heuristic analysis (deprecated) |
| POST | `/analyze` | **Production:** Whisper + Phoneme analysis |

**Production Endpoint Features:**
- Whisper Speech-to-Text recognition (local)
- Phonemizer-based ground-truth phonemes
- Acoustic feature extraction (MFCC, pitch, formants)
- Per-phoneme alignment and scoring
- Overall pronunciation grade (A-F)
- Confidence scores and detailed feedback

**Example Request:**
```bash
curl -X POST http://localhost:8000/analyze \
  -F "file=@recording.wav" \
  -F "word=pencere"
```

**Example Response:**
```json
{
  "word": "pencere",
  "recognized_text": "pencere",
  "recognition_confidence": 0.91,
  "phonemes_target": "p e n d͡ʒ e ɾ e",
  "segment_scores": {
    "p": 0.96,
    "e": 0.91,
    "n": 0.90,
    "d͡ʒ": 0.88,
    "ɾ": 0.85
  },
  "overall": 0.88,
  "grade": "B (İyi)",
  "analysis_method": "whisper_hybrid"
}
```

**See:** `docs/guides/PRONUNCIATION_ANALYSIS_GUIDE.md` for complete documentation

## 🎨 Features

✅ **Modern UI** - Material UI components with beautiful design
✅ **Audio Recording** - Browser MediaRecorder API
✅ **Real-time Feedback** - Instant pronunciation analysis
✅ **Phoneme Visualization** - IPA phoneme generation with eSpeak-NG
✅ **Data Privacy** - KVKK compliant, all processing local
✅ **Zero Cost** - No API fees, runs completely offline
✅ **Open Source** - Built with open-source tools (Whisper, Phonemizer)
✅ **Scalable** - Modular architecture, easy to extend  

## 🧪 Testing

### Backend
```bash
cd backend
pytest
```

### Frontend
```bash
cd frontend
npm run test
```

## 📝 Development Notes

### Adding New Words

Edit `frontend/src/components/PronunciationTest.tsx`:
```typescript
const turkishWords = [
  'araba', 'bahçe', // ... add more words
]
```

### Custom Feature Extraction

Modify `extract_acoustic_features()` in:
- `backend/inference.py` - Acoustic analysis logic

### Phoneme Customization

Edit `_generate_phonemes_espeak()` in `backend/inference.py`:
```python
phonemes = phonemize(
    word,
    language='tr',  # Change language
    backend='espeak',
    with_stress=True  # Enable stress markers
)
```

## 🔒 Data Privacy & KVKK Compliance

- All participant data anonymized with UUID
- Audio stored locally, not shared
- Consent explicitly required
- Data used only for research
- Participant can withdraw anytime

## 🌐 Deployment

### Production Backend

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Production Frontend

```bash
cd frontend
npm run build
# Deploy /dist folder to hosting service
```

**Recommended hosts:**
- Frontend: Vercel, Netlify, Cloudflare Pages
- Backend: Railway, Render, DigitalOcean

## 📚 Documentation

Comprehensive documentation is available in the [`docs/`](docs/) folder:

### Quick Links
- 📖 **[Documentation Index](docs/README.md)** - Complete documentation guide
- 🚀 **[Quick Start](docs/setup/QUICK_START.md)** - Get started in 5 minutes
- 🎯 **[Pronunciation Guide](docs/guides/PRONUNCIATION_ANALYSIS_GUIDE.md)** - Using the analysis API
- 🔄 **[Whisper Migration](docs/MIGRATION_TO_WHISPER.md)** - Azure to Whisper migration guide
- 🔧 **[Setup Guide](docs/setup/SETUP_GUIDE.md)** - Detailed installation
- 🏗️ **[Architecture](docs/architecture/SYSTEM_OVERVIEW.md)** - System design
- 🗂️ **[Deprecated](docs/deprecated/)** - Archived ML training and Azure docs

### API Documentation
- **Interactive API Docs:** http://localhost:8000/docs (when backend running)
- **Phoneme API:** See [Phoneme Feature Guide](docs/guides/PHONEME_FEATURE.md)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m "Add feature"`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

Created by PhoneticHybrid Team for Turkish linguistics research.

## 🙏 Acknowledgments

- **OpenAI Whisper** - Open-source speech recognition
- **Phonemizer** - IPA transcription (eSpeak NG)
- **Praat** - Phonetic analysis toolkit
- **librosa** - Audio feature extraction
- **Material UI** - React component library
- **FastAPI** - Modern Python web framework

## 📞 Support

For issues and questions:
- Open GitHub issue
- Check documentation in `docs/` folder
- Review API docs at http://localhost:8000/docs

---

**Built with ❤️ for Turkish language research**
