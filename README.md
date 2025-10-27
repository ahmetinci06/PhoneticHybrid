# PhoneticHybrid 🎙️

A production-ready Turkish pronunciation analysis platform using **Azure Speech Services** + **Phonemizer** for academic phoneme-level pronunciation assessment.

## 🎯 Overview

PhoneticHybrid is a full-stack web platform where participants:
1. Record Turkish words
2. Audio is analyzed using Azure Cognitive Services Speech-to-Text
3. Receive detailed phoneme-level pronunciation feedback
4. Get actionable insights based on acoustic features

**Perfect for:** Linguistic research, speech therapy, language learning applications, pronunciation assessment

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────┐
│              NEW AZURE-BASED ARCHITECTURE                     │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌──────────────┐      ┌──────────────┐      ┌────────────┐ │
│  │   Frontend   │─────▶│   Backend    │─────▶│   Azure    │ │
│  │ React + MUI  │◀─────│   FastAPI    │◀─────│  Speech AI │ │
│  └──────────────┘      └──────────────┘      └────────────┘ │
│                               │                                │
│                               ├─────▶ Phonemizer (eSpeak NG)  │
│                               ├─────▶ Acoustic Analysis       │
│                               │       (librosa, Praat)        │
│                               └─────▶ Phoneme Alignment       │
│                                                                │
└──────────────────────────────────────────────────────────────┘
```

### Tech Stack

**Frontend:**
- React 18
- Material UI v6
- TypeScript
- Vite

**Backend:**
- FastAPI (Python 3.10+)
- Azure Cognitive Services Speech SDK
- Phonemizer (eSpeak NG backend)
- librosa (audio processing)
- praat-parselmouth (phonetic analysis)
- scipy (phoneme alignment)

**Analysis Pipeline:**
- Azure Speech-to-Text (tr-TR)
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
- **Google Account** (for Colab training)

### 1. Clone Repository

```bash
cd phoneizer
```

### 2. Setup Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Azure Speech Services

1. Create an Azure account: https://portal.azure.com
2. Create a **Speech** resource
3. Copy your **Key** and **Region**
4. Create `.env` file in `/backend`:

```bash
cp .env.example .env
```

5. Edit `.env` and add your credentials:

```
AZURE_SPEECH_KEY=your_actual_key_here
AZURE_REGION=your_region_here
```

### 4. Setup Frontend

```bash
cd frontend
npm install
```

### 5. Run Development Servers

**Backend:**
```bash
cd backend
python main.py
# Server runs at http://localhost:8000
```

**Frontend:**
```bash
cd frontend
npm run dev
# App runs at http://localhost:3000
```

### 6. Access Application

Open browser: **http://localhost:3000**

## 🎓 How It Works (New Azure-Based Approach)

### Analysis Pipeline

1. **Speech Recognition** (Azure)
   - Audio sent to Azure Speech-to-Text API
   - Turkish language model (tr-TR)
   - Returns recognized text + confidence score

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
   - Combine Azure confidence with acoustic scores
   - Generate per-phoneme feedback

5. **Overall Assessment**
   - Weighted score: 40% Azure + 60% Acoustic
   - Letter grade (A-F)
   - Detailed phoneme breakdown

### Migration from Old ML Training Approach

The previous custom ML training workflow has been **deprecated** and moved to `/backend/deprecated/`. The new approach offers:

✅ **No training required** - Use Azure's pre-trained models  
✅ **Better accuracy** - Production-grade speech recognition  
✅ **Phoneme-level detail** - Granular feedback per sound  
✅ **Easier deployment** - Just configure API keys  
✅ **Scalable** - Cloud-based processing

**Old files archived in:** `/backend/deprecated/` and `/ml_colab/`

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
| POST | `/analyze/audio` | Legacy heuristic analysis |
| POST | `/analyze/azure` | **NEW:** Azure + Phoneme analysis |

**New Azure Endpoint Features:**
- Azure Speech-to-Text recognition
- Phonemizer-based ground-truth phonemes
- Acoustic feature extraction (MFCC, pitch, formants)
- Per-phoneme alignment and scoring
- Overall pronunciation grade (A-F)
- Confidence scores and detailed feedback

**Example Request:**
```bash
curl -X POST http://localhost:8000/analyze/azure \
  -F "file=@recording.wav" \
  -F "word=pencere"
```

**Example Response:**
```json
{
  "word": "pencere",
  "recognized_text": "pencere",
  "azure_confidence": 0.91,
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
  "analysis_method": "azure_hybrid"
}
```

**See:** `PRONUNCIATION_ANALYSIS_GUIDE.md` for complete documentation

## 🎨 Features

✅ **Modern UI** - Material UI components with beautiful design  
✅ **Audio Recording** - Browser MediaRecorder API  
✅ **Real-time Feedback** - Instant pronunciation analysis  
✅ **Phoneme Visualization** - IPA phoneme generation with eSpeak-NG  
✅ **Data Privacy** - KVKK compliant, encrypted storage  
✅ **GPU Training** - Fast model training on Colab  
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

### Configuring Azure Credentials

Edit `backend/.env`:
```bash
AZURE_SPEECH_KEY=your_key_here
AZURE_REGION=eastus  # or your region
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
- ☁️ **[Azure Integration](docs/azure/AZURE_INTEGRATION_SUMMARY.md)** - Complete Azure setup
- 🎯 **[Pronunciation Guide](docs/guides/PRONUNCIATION_ANALYSIS_GUIDE.md)** - Using the analysis API
- 🔧 **[Setup Guide](docs/setup/SETUP_GUIDE.md)** - Detailed installation
- 🏗️ **[Architecture](docs/architecture/SYSTEM_OVERVIEW.md)** - System design
- 🗂️ **[Deprecated ML Training](docs/deprecated/)** - Archived ML training docs

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

- **Azure Cognitive Services** - Speech recognition
- **Phonemizer** - IPA transcription (eSpeak NG)
- **Praat** - Phonetic analysis toolkit
- **librosa** - Audio feature extraction
- **Material UI** - React component library
- **FastAPI** - Modern Python web framework

## 📞 Support

For issues and questions:
- Open GitHub issue
- Check documentation in `ml_colab/`
- Review API docs at `/docs` endpoint

---

**Built with ❤️ for Turkish language research**
