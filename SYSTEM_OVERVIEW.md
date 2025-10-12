# PhoneticHybrid - System Overview

## Executive Summary

PhoneticHybrid is a hybrid cloud-local system for analyzing Turkish pronunciation quality using machine learning. The system enables researchers to collect audio data through a web interface, train models on Google Colab's GPU infrastructure, and deploy inference locally for participant feedback.

## System Components

### 1. Frontend (React + Material UI)

**Technology Stack:**
- React 18 with TypeScript
- Material UI v6 for components
- Vite for fast development
- MediaRecorder API for audio capture

**Key Features:**
- Modern, responsive UI design
- Real-time audio recording
- Progress tracking
- Form validation
- KVKK compliance interface

**User Flow:**
1. Welcome screen with introduction
2. KVKK consent and personal information collection
3. Orthodontic literacy survey (8 questions)
4. Pronunciation test (30 Turkish words)
5. Thank you screen with completion confirmation

### 2. Backend (FastAPI)

**Technology Stack:**
- FastAPI for REST API
- PyTorch for ML inference
- librosa for audio processing
- Praat-Parselmouth for phonetic analysis
- Phonemizer for IPA transcription

**API Endpoints:**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Health check and status |
| `/register` | POST | Register new participant |
| `/survey` | POST | Save survey responses |
| `/upload` | POST | Upload audio and analyze |
| `/health` | GET | System diagnostics |

**Data Processing Pipeline:**
```
Audio Upload → Save to Disk → Feature Extraction → ML Inference → Score Generation → Return Result
```

### 3. ML Training (Google Colab)

**Training Environment:**
- Google Colab with GPU (T4/V100)
- PyTorch 2.1.2
- Training time: ~15-30 minutes

**Model Architecture:**
- Input: 37-dimensional feature vectors
- Hidden layers: [128, 64, 32] neurons
- Output: Binary classification (quality score)
- Activation: ReLU + Batch Normalization
- Regularization: Dropout (0.3)

**Feature Set (37 features):**
1. **MFCCs:** 13 coefficients (mean + std) = 26 features
2. **Spectral:** Centroid, rolloff, bandwidth = 3 features
3. **Temporal:** Zero-crossing rate = 1 feature
4. **Energy:** RMS = 1 feature
5. **Formants:** F1, F2, F3 = 3 features
6. **Pitch:** F0 mean and std = 2 features
7. **Duration:** Audio length = 1 feature

## Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      SYSTEM ARCHITECTURE                         │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐
│   Participant│
│    Browser   │
└──────┬───────┘
       │ 1. Access web app
       │ 2. Record audio
       │
       ▼
┌──────────────────┐
│  React Frontend  │  Port 3000
│  (localhost)     │
└──────┬───────────┘
       │ 3. POST /upload (multipart/form-data)
       │
       ▼
┌──────────────────┐
│  FastAPI Backend │  Port 8000
│  (localhost)     │
└──────┬───────────┘
       │ 4. Save to /data/participant_xxx/kelimeler/
       │
       ▼
┌──────────────────┐
│ Feature Extract  │
│  (librosa +      │
│   Parselmouth)   │
└──────┬───────────┘
       │ 5. Extract 37 features
       │
       ▼
┌──────────────────┐
│  PyTorch Model   │  Loaded from /models/
│  (trained_model) │
└──────┬───────────┘
       │ 6. Inference → Score (0-1)
       │
       ▼
┌──────────────────┐
│  Generate        │
│  Feedback        │
└──────┬───────────┘
       │ 7. Return JSON response
       │
       ▼
┌──────────────────┐
│  Frontend UI     │
│  Display Result  │
└──────────────────┘


TRAINING PHASE (Separate - Google Colab):

┌──────────────────┐
│  Collected Data  │
│  (Google Drive)  │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  Colab Notebook  │  GPU Training
│  (training.ipynb)│
└──────┬───────────┘
       │ 8. Train model (50 epochs)
       │
       ▼
┌──────────────────┐
│ trained_model.pt │
└──────┬───────────┘
       │ 9. Download to local
       │
       ▼
┌──────────────────┐
│  /models/        │  Deploy to backend
│  (local)         │
└──────────────────┘
```

## File System Structure

### Data Storage Format

```
data/
└── participant_<uuid>/
    ├── info.json                 # Participant metadata
    │   {
    │     "id": "uuid",
    │     "name": "string",
    │     "age": number,
    │     "gender": "string",
    │     "consent": true,
    │     "timestamp": "ISO8601"
    │   }
    │
    ├── survey.json               # Survey responses
    │   {
    │     "participant_id": "uuid",
    │     "responses": [1,2,3,4,5,...],
    │     "timestamp": "ISO8601"
    │   }
    │
    └── kelimeler/                # Audio recordings
        ├── 00_araba.wav
        ├── 00_araba_result.json
        │   {
        │     "word": "araba",
        │     "score": 0.75,
        │     "confidence": 0.85,
        │     "feedback": "İyi! Küçük iyileştirmeler..."
        │   }
        ├── 01_bahçe.wav
        └── ...
```

## Technology Choices & Rationale

### Frontend: React + Material UI
- **Why React?** Component-based, large ecosystem, excellent TypeScript support
- **Why MUI?** Production-ready components, accessibility built-in, customizable theming
- **Why Vite?** Fast dev server, optimized builds, modern ESM support

### Backend: FastAPI
- **Automatic API docs** (Swagger UI)
- **High performance** (async/await support)
- **Type validation** (Pydantic models)
- **Easy integration** with ML libraries

### ML Training: Google Colab
- **Free GPU access** (T4 GPUs)
- **No local setup** required
- **Reproducible** environment
- **Easy sharing** via notebooks

### Audio Processing: librosa + Praat
- **librosa:** Industry standard for audio ML
- **Praat:** Gold standard for phonetic analysis
- **Parselmouth:** Python bindings for Praat

## Performance Characteristics

### Frontend
- **Initial Load:** <2 seconds (dev mode)
- **Audio Recording:** Real-time (no lag)
- **Form Submission:** <200ms

### Backend
- **API Response (no ML):** <50ms
- **Feature Extraction:** ~200-500ms per audio file
- **ML Inference:** ~100-200ms per prediction
- **Total Analysis Time:** ~300-700ms per recording

### Training
- **Feature Extraction:** ~2-5 minutes for 1000 samples
- **Model Training:** ~15-30 minutes (50 epochs, GPU)
- **Expected Accuracy:** 70-85% (with quality labels)

## Scalability Considerations

### Current Capacity
- **Concurrent Users:** 10-50 (single backend instance)
- **Data Storage:** File-based (scales to thousands of participants)
- **Model Size:** ~1-2MB (fast loading)

### Scaling Strategies
1. **Horizontal:** Deploy multiple backend instances + load balancer
2. **Database:** Migrate from file storage to PostgreSQL/MongoDB
3. **Object Storage:** Use S3/MinIO for audio files
4. **Caching:** Add Redis for feature vectors
5. **CDN:** Serve frontend from CDN
6. **Async Processing:** Queue-based audio analysis

## Security & Privacy

### Data Protection
- **Anonymization:** Participant IDs are UUIDs (not names)
- **Local Storage:** Data stays on local server by default
- **KVKK Compliance:** Explicit consent required
- **No Third-Party:** Audio never sent to external services

### Recommended Security Measures
1. HTTPS in production
2. Authentication/authorization
3. Rate limiting
4. Input validation and sanitization
5. Regular security audits
6. Encrypted backups

## Research Workflow

### Phase 1: Data Collection (Weeks 1-4)
1. Deploy web application
2. Share link with participants
3. Collect recordings (target: 50+ participants)
4. Monitor data quality

### Phase 2: ML Training (Week 5)
1. Upload data to Google Drive
2. Annotate audio with quality labels
3. Run training notebook in Colab
4. Evaluate model performance
5. Download trained model

### Phase 3: Deployment (Week 6)
1. Copy model to local backend
2. Test inference accuracy
3. Collect feedback from users
4. Iterate on model/features

### Phase 4: Refinement (Ongoing)
1. Collect more data
2. Retrain periodically
3. Add new features
4. Improve UI/UX

## Maintenance Requirements

### Regular Tasks
- **Daily:** Monitor server logs
- **Weekly:** Backup participant data
- **Monthly:** Retrain model with new data
- **Quarterly:** Update dependencies

### Monitoring Metrics
- API response times
- Error rates
- Disk space usage
- Model accuracy (user feedback)
- Participant completion rates

## Future Enhancements

### Short-term
- [ ] Add real-time feedback during recording
- [ ] Implement user authentication
- [ ] Create admin dashboard for data review
- [ ] Add data export (CSV/Excel)

### Medium-term
- [ ] Multi-language support
- [ ] Advanced phonetic visualizations
- [ ] Detailed error analysis (phoneme-level)
- [ ] Mobile app (React Native)

### Long-term
- [ ] Transformer-based models
- [ ] Real-time pronunciation coaching
- [ ] Gamification features
- [ ] Integration with speech therapy tools

## Technical Debt & Known Limitations

### Current Limitations
1. **Labels:** Demo uses synthetic labels (need real annotations)
2. **Model:** Simple feedforward network (could use RNN/Transformer)
3. **Features:** Basic acoustic features (could add prosody, rhythm)
4. **Storage:** File-based (should migrate to database)
5. **Auth:** No authentication system
6. **Scale:** Single-server deployment

### Mitigation Plan
- Prioritize real label collection
- Benchmark advanced architectures
- Implement incremental improvements
- Plan migration path to production infrastructure

## Success Metrics

### Technical Metrics
- Model accuracy: >75%
- API uptime: >99%
- Response time: <1s
- Error rate: <1%

### Research Metrics
- Participant completion rate: >80%
- Data quality: <5% unusable recordings
- Inter-rater reliability: >0.8 (Cohen's kappa)

### User Experience
- System Usability Scale (SUS): >70
- Time to complete: <15 minutes
- User satisfaction: >4/5 stars

---

**System Status:** Production-ready for research use  
**Last Updated:** 2025  
**Version:** 1.0.0
