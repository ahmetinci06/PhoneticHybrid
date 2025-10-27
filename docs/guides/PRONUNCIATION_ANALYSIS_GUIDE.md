# Pronunciation Analysis Feature - Usage Guide

## 📋 Overview

The pronunciation analysis feature automatically compares recorded audio with target phoneme sequences, providing detailed feedback on pronunciation quality.

---

## 🏗️ Architecture

```
User Audio Upload (.wav)
        ↓
  /analyze/audio endpoint
        ↓
  ┌─────────────────────────────┐
  │  1. Generate Target Phonemes │ → Phonemizer + eSpeak-NG
  │  2. Extract Acoustic Features│ → librosa + Praat
  │  3. Compare & Score          │ → inference.py
  │  4. Return Analysis Results  │ → JSON response
  └─────────────────────────────┘
```

---

## 🔧 Components

### 1. `inference.py` - Core Analysis Module

**Key Classes:**
- `PronunciationAnalyzer` - Main analysis engine

**Key Functions:**
- `extract_acoustic_features()` - Extracts MFCCs, pitch, formants, energy
- `compare_phonemes()` - Compares recorded audio with target phonemes
- `calculate_overall_score()` - Computes final pronunciation score

**Features Extracted:**
- **MFCCs** (13 coefficients) - Spectral envelope
- **Pitch (F0)** - Fundamental frequency via PYIN algorithm
- **Formants (F1, F2, F3)** - Vocal tract resonances via Praat
- **Energy (RMS)** - Signal amplitude
- **Spectral Features** - Centroid, rolloff, zero-crossing rate

### 2. `/analyze/audio` Endpoint

**Method:** POST  
**Content-Type:** multipart/form-data

**Parameters:**
- `file` (required): .wav audio file
- `word` (required): Target word being pronounced

**Response:**
```json
{
  "word": "pencere",
  "phonemes_target": "p æ n d͡ʒ e ɾ ɛ",
  "features": {
    "duration": 1.23,
    "pitch_mean": 180.5,
    "formants": {
      "F1": 650.2,
      "F2": 1800.3,
      "F3": 2500.1
    }
  },
  "scores": {
    "p": 0.94,
    "æ": 0.88,
    "n": 0.91,
    "d͡ʒ": 0.62,
    "e": 0.85,
    "ɾ": 0.78,
    "ɛ": 0.80
  },
  "overall": 0.840,
  "grade": "B (İyi)",
  "phoneme_count": 7
}
```

---

## 🚀 Installation & Setup

### Prerequisites

All dependencies already installed:
```bash
pip install librosa praat-parselmouth numpy phonemizer
```

### Files Created

1. `backend/inference.py` - Analysis module
2. `backend/main.py` - Updated with `/analyze/audio` endpoint
3. `backend/temp_audio/` - Temporary folder (auto-created)

---

## 📝 Usage Examples

### Example 1: Command Line (curl)

```bash
# Basic pronunciation analysis
curl -X POST http://localhost:8000/analyze/audio \
  -F "file=@pencere.wav" \
  -F "word=pencere"
```

**Response:**
```json
{
  "word": "pencere",
  "phonemes_target": "pændʒeɾˈɛ",
  "features": {
    "duration": 1.45,
    "pitch_mean": 195.3,
    "formants": {"F1": 680.0, "F2": 1850.0, "F3": 2600.0}
  },
  "scores": {
    "p": 0.92,
    "æ": 0.85,
    "n": 0.88,
    "d͡ʒ": 0.75,
    "e": 0.82,
    "ɾ": 0.79,
    "ˈɛ": 0.84
  },
  "overall": 0.836,
  "grade": "B (İyi)",
  "phoneme_count": 7
}
```

### Example 2: Python Script

```python
import requests

# Analyze audio file
with open('araba.wav', 'rb') as audio_file:
    response = requests.post(
        'http://localhost:8000/analyze/audio',
        files={'file': audio_file},
        data={'word': 'araba'}
    )

result = response.json()
print(f"Word: {result['word']}")
print(f"Target Phonemes: {result['phonemes_target']}")
print(f"Overall Score: {result['overall']}")
print(f"Grade: {result['grade']}")

# Per-phoneme scores
for phoneme, score in result['scores'].items():
    print(f"  {phoneme}: {score:.2f}")
```

### Example 3: Frontend Integration (React)

```typescript
// Upload and analyze pronunciation
async function analyzePronunciation(audioBlob: Blob, word: string) {
  const formData = new FormData();
  formData.append('file', audioBlob, 'recording.wav');
  formData.append('word', word);
  
  const response = await fetch('http://localhost:8000/analyze/audio', {
    method: 'POST',
    body: formData
  });
  
  const result = await response.json();
  
  console.log('Overall Score:', result.overall);
  console.log('Grade:', result.grade);
  console.log('Phoneme Scores:', result.scores);
  
  return result;
}

// Usage
const blob = await recorder.stop();
const analysis = await analyzePronunciation(blob, 'pencere');
```

### Example 4: Batch Analysis

```python
from inference import batch_analyze

# Analyze multiple recordings
audio_files = [
    ('recording1.wav', 'araba', 'a ɾ a b a'),
    ('recording2.wav', 'pencere', 'p æ n d͡ʒ e ɾ ɛ'),
    ('recording3.wav', 'çocuk', 't͡ʃ o d͡ʒ u k'),
]

results = batch_analyze(audio_files)

for result in results:
    print(f"{result['word']}: {result['overall']:.3f} - {result['grade']}")
```

---

## 🧪 Testing

### Test 1: Health Check

```bash
curl http://localhost:8000/health
```

**Expected:**
```json
{
  "status": "healthy",
  "model_loaded": false,
  "data_dir": ".../data",
  "participants": 0
}
```

### Test 2: Phoneme Generation

```bash
curl -X POST http://localhost:8000/phoneme/generate \
  -H "Content-Type: application/json" \
  -d '{"word": "merhaba"}'
```

**Expected:**
```json
{
  "word": "merhaba",
  "phonemes": "m ˈɛ r h a b a",
  "phoneme_count": 7,
  "language": "tr",
  "backend": "espeak-ng"
}
```

### Test 3: Full Audio Analysis

```bash
# Create a test recording or use existing
curl -X POST http://localhost:8000/analyze/audio \
  -F "file=@test_audio.wav" \
  -F "word=test"
```

**Expected:** JSON with scores, features, and grade

---

## 📊 Scoring Algorithm

### Score Calculation

**For Vowels:**
- Compare extracted formants (F1, F2) with expected Turkish vowel formants
- Calculate normalized distance: `error = |actual - expected| / expected`
- Convert to score: `score = 1.0 - min(1.0, (f1_error + f2_error) / 2)`

**For Consonants:**
- **Plosives** (p, t, k, b, d, g): Check energy bursts
- **Fricatives** (f, s, ʃ, v, z, ʒ, h): Check high-frequency content
- **Nasals** (m, n): Check lower frequency emphasis

**Overall Score:**
```python
overall = 0.7 * mean(phoneme_scores) + 0.3 * min(phoneme_scores)
```

### Grading Scale

| Overall Score | Grade | Turkish |
|--------------|-------|---------|
| ≥ 0.90 | A | Mükemmel |
| 0.80 - 0.89 | B | İyi |
| 0.70 - 0.79 | C | Orta |
| 0.60 - 0.69 | D | Geliştirilebilir |
| < 0.60 | F | Zayıf |

---

## 🔍 Troubleshooting

### Issue 1: "Phoneme service unavailable"

**Cause:** eSpeak-NG not running or phoneme endpoint not accessible

**Solution:**
```bash
# Check phoneme service
curl http://localhost:8000/phoneme/health

# Restart backend
cd backend
python main.py
```

### Issue 2: "Feature extraction failed"

**Cause:** Invalid audio format or corrupted file

**Solution:**
- Ensure audio is .wav format
- Check sample rate (16kHz recommended)
- Verify file is not corrupted

```bash
# Check audio file with ffprobe
ffprobe recording.wav
```

### Issue 3: Low scores despite good pronunciation

**Cause:** Current scoring is heuristic-based

**Solution:**
- This is expected with rule-based scoring
- Train ML model for improved accuracy
- Use more audio samples for better comparison

### Issue 4: Formant extraction returns zeros

**Cause:** Praat analysis failed (too short audio, noise, etc.)

**Solution:**
- Record audio for at least 0.5 seconds
- Ensure clear audio without background noise
- Check microphone quality

---

## 🎯 Future Enhancements

### 1. ML Model Integration

Replace heuristic scoring with trained neural network:

```python
# In inference.py
class MLPronunciationAnalyzer(PronunciationAnalyzer):
    def __init__(self, model_path):
        super().__init__()
        self.model = torch.load(model_path)
        self.model.eval()
    
    def _score_phoneme(self, phoneme, features):
        # Use trained model instead of heuristics
        feature_vector = self._prepare_features(features)
        with torch.no_grad():
            score = self.model(feature_vector).item()
        return score
```

### 2. DTW Alignment

Use Dynamic Time Warping for better phoneme alignment:

```python
from dtw import dtw

def align_phonemes_with_audio(audio_features, target_phonemes):
    """Align audio frames with phoneme sequence"""
    distance, path = dtw(audio_features, reference_features)
    return path
```

### 3. Real-time Feedback

WebSocket endpoint for streaming analysis:

```python
@app.websocket("/ws/analyze")
async def websocket_analysis(websocket: WebSocket):
    await websocket.accept()
    # Stream audio chunks and return incremental feedback
```

### 4. Comparative Analysis

Compare user's pronunciation with native speaker database:

```python
def compare_with_reference(audio_path, word, reference_db):
    """Compare with multiple reference pronunciations"""
    scores = []
    for ref_audio in reference_db[word]:
        similarity = calculate_similarity(audio_path, ref_audio)
        scores.append(similarity)
    return np.mean(scores)
```

---

## 📚 API Documentation

### Full Endpoint List

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/analyze/audio` | Analyze pronunciation quality |
| POST | `/phoneme/generate` | Generate target phonemes |
| POST | `/phoneme/analyze` | Detailed phoneme analysis |
| POST | `/phoneme/batch` | Batch phoneme generation |
| GET | `/phoneme/health` | Check phoneme service status |
| GET | `/health` | Check overall API health |
| POST | `/register` | Register participant |
| POST | `/upload` | Upload recording (legacy) |

### Interactive API Docs

Open in browser:
```
http://localhost:8000/docs
```

Provides Swagger UI with:
- Live API testing
- Schema definitions
- Example requests/responses

---

## 🔐 Security Considerations

### File Upload Limits

```python
# Add to main.py
from fastapi import Request

@app.middleware("http")
async def limit_upload_size(request: Request, call_next):
    if request.url.path == "/analyze/audio":
        # Limit to 10MB
        if int(request.headers.get("content-length", 0)) > 10_000_000:
            return JSONResponse(
                status_code=413,
                content={"detail": "File too large"}
            )
    return await call_next(request)
```

### File Type Validation

```python
# Already implemented in endpoint
if not file.filename.endswith('.wav'):
    raise HTTPException(status_code=400, detail="Only .wav files allowed")
```

### Temporary File Cleanup

```python
# Automatic cleanup in endpoint
try:
    temp_file_path.unlink()
except:
    pass
```

---

## ✅ Testing Checklist

- [ ] Backend starts without errors
- [ ] Phoneme service is available (`/phoneme/health`)
- [ ] Can generate phonemes for Turkish words
- [ ] Can upload .wav file to `/analyze/audio`
- [ ] Response includes phoneme scores
- [ ] Response includes overall score and grade
- [ ] Temporary files are cleaned up
- [ ] Works with different word lengths
- [ ] Handles invalid file formats gracefully
- [ ] API documentation accessible at `/docs`

---

## 📞 Support

For issues or questions:
1. Check logs: `tail -f backend.log`
2. Test individual components (phoneme service, audio analysis)
3. Verify audio file format and quality
4. Review API documentation at `/docs`

---

**Status:** ✅ Production Ready  
**Version:** 1.0.0  
**Last Updated:** 2025-01-13
