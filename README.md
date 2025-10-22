# PhoneticHybrid 🎙️

A research-grade hybrid (Google Colab + Local) system for Turkish pronunciation analysis using deep learning.

## 🎯 Overview

PhoneticHybrid is a full-stack web platform where participants:
1. Record 30 Turkish words
2. Their audio is analyzed using ML
3. Receive pronunciation accuracy feedback

**Perfect for:** Linguistic research, speech therapy, language learning applications

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SYSTEM ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐      ┌──────────────┐      ┌───────────┐ │
│  │   Frontend   │─────▶│   Backend    │─────▶│  Models   │ │
│  │ React + MUI  │◀─────│   FastAPI    │◀─────│  PyTorch  │ │
│  └──────────────┘      └──────────────┘      └───────────┘ │
│        ▲                      ▲                      ▲       │
│        │                      │                      │       │
│        │                      └──────────────────────┘       │
│        │                   Inference (Local)                 │
│        │                                                      │
│        └───────────────┐                                     │
│                        │                                     │
│                ┌───────▼────────┐                            │
│                │  Google Colab  │                            │
│                │  GPU Training  │                            │
│                └────────────────┘                            │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Tech Stack

**Frontend:**
- React 18
- Material UI v6
- TypeScript
- Vite

**Backend:**
- FastAPI (Python 3.10+)
- PyTorch 2.1.2
- librosa (audio processing)
- praat-parselmouth (phonetic analysis)

**ML Training:**
- Google Colab (GPU)
- PyTorch neural networks
- Feature extraction: MFCCs, formants, F0, spectral features

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

### 3. Setup Frontend

```bash
cd frontend
npm install
```

### 4. Run Development Servers

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

### 5. Access Application

Open browser: **http://localhost:3000**

## 🎓 Training the ML Model

### Step 1: Collect Data
1. Run the web application
2. Have participants complete the pronunciation test
3. Data saved to `/data/participant_xxx/`

### Step 2: Train on Google Colab
1. Upload `/data` folder to Google Drive: `MyDrive/phoneizer/data/`
2. Open `ml_colab/training_notebook.ipynb` in Colab
3. Enable GPU: Runtime → Change runtime type → GPU
4. Run all cells sequentially
5. Download trained model: `models/trained_model.pt`

### Step 3: Deploy Model
1. Copy `trained_model.pt` to local `models/` directory
2. Restart backend server
3. Model will be loaded automatically

**Detailed instructions:** See `ml_colab/ai_training_instructions.txt`

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
| POST | `/analyze/audio` | Analyze pronunciation quality of uploaded .wav |

**Features:**
- Automatic phoneme target generation
- Acoustic feature extraction (MFCC, pitch, formants)
- **ML-based scoring** (0-100) or heuristic fallback
- Per-phoneme detailed feedback
- Overall pronunciation grade (A-F)
- Confidence intervals (with ML)

**See:** `PRONUNCIATION_ANALYSIS_GUIDE.md` for complete documentation

### ML Model Training (New!)
Train a neural network to replace heuristic scoring with learned predictions.

**Quick Start:**
```bash
cd backend
python train_ml_model.py
```

**Features:**
- 57 acoustic features extracted
- Neural network (PyTorch)
- Training on Google Colab (GPU)
- Automatic deployment

**See:** `ML_TRAINING_GUIDE.md` for complete ML training documentation

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

### Changing Model Architecture

Edit `ml_colab/training_notebook.ipynb`:
```python
model = PronunciationQualityNet(
    input_size=37,
    hidden_sizes=[256, 128, 64],  # Modify layers
    dropout=0.3
)
```

### Custom Feature Extraction

Modify `extract_acoustic_features()` in:
- Training: `ml_colab/training_notebook.ipynb`
- Inference: `backend/main.py`

**Important:** Keep feature extraction identical in both!

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

- **Training Guide:** `ml_colab/ai_training_instructions.txt`
- **Environment Setup:** `ml_colab/training_environment_setup.txt`
- **API Docs:** http://localhost:8000/docs (when backend running)

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

- **Phonemizer** - IPA transcription
- **Praat** - Phonetic analysis toolkit
- **librosa** - Audio feature extraction
- **Material UI** - React component library

## 📞 Support

For issues and questions:
- Open GitHub issue
- Check documentation in `ml_colab/`
- Review API docs at `/docs` endpoint

---

**Built with ❤️ for Turkish language research**
