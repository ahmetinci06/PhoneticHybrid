# PhoneticHybrid Setup Guide 🚀

Complete setup instructions for the Turkish Pronunciation Analysis system.

## 📋 Prerequisites Checklist

Before starting, ensure you have:

- [ ] **Node.js** 18.x or higher
- [ ] **Python** 3.10 or higher
- [ ] **Git** (for version control)
- [ ] **Google Account** (for Colab training)
- [ ] **Text Editor** (VS Code recommended)
- [ ] **Modern Browser** (Chrome/Firefox with microphone access)

## 🔧 Installation Steps

### 1. Backend Setup

#### Install Python Dependencies

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Install System Dependencies (for phonemizer)

**Windows:**
```bash
# Install espeak-ng using Chocolatey
choco install espeak-ng

# Or download installer from:
# https://github.com/espeak-ng/espeak-ng/releases
```

**macOS:**
```bash
brew install espeak
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install espeak-ng
```

#### Verify Installation

```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
python -c "import librosa; print(f'librosa: {librosa.__version__}')"
python -c "import parselmouth; print('Praat: OK')"
```

Expected output:
```
PyTorch: 2.1.2
librosa: 0.10.1
Praat: OK
```

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Verify installation
npm list react react-dom @mui/material
```

Expected packages installed:
- react@18.x
- react-dom@18.x
- @mui/material@6.x

### 3. Create Required Directories

```bash
# From project root
mkdir -p data models

# Create placeholder files
touch data/.gitkeep
touch models/.gitkeep
```

## 🏃 Running the Application

### Start Backend Server

```bash
cd backend
python main.py
```

Expected output:
```
INFO:     Started server process
INFO:     Waiting for application startup.
⚠ Model not found. Train the model first using the Colab notebook.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ Backend ready at: **http://localhost:8000**

### Start Frontend Development Server

Open a new terminal:

```bash
cd frontend
npm run dev
```

Expected output:
```
  VITE v5.0.12  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

✅ Frontend ready at: **http://localhost:3000**

## 🧪 Verify Setup

### Test Backend API

```bash
curl http://localhost:8000/
```

Expected response:
```json
{
  "service": "Turkish Pronunciation Analysis",
  "status": "running",
  "model_loaded": false
}
```

### Test Frontend

1. Open browser: http://localhost:3000
2. You should see the Welcome screen
3. Click "Başlamak İçin Tıklayın"
4. Consent form should appear

## 🎓 Training Your First Model

### 1. Collect Sample Data

1. Run the web app (frontend + backend)
2. Complete the flow as a test participant:
   - Fill consent form
   - Complete survey
   - Record at least 5 words (for testing)
3. Check `data/` directory for participant folder

### 2. Upload Data to Google Drive

```bash
# Zip your data folder (optional)
zip -r phoneizer_data.zip data/

# Upload to Google Drive:
# MyDrive/phoneizer/data/
```

### 3. Open Training Notebook

1. Go to: https://colab.research.google.com
2. Upload: `ml_colab/training_notebook.ipynb`
3. Enable GPU:
   - Runtime → Change runtime type
   - Hardware accelerator: **GPU**
   - Click **Save**

### 4. Run Training

Execute cells in order:
1. **Setup & Dependencies** - Install packages
2. **Mount Drive** - Grant permissions
3. **Load Data** - Verify data loaded
4. **Feature Extraction** - Wait for progress bar
5. **Labels** - ⚠️ Replace with real labels!
6. **Training** - Watch for 15-30 minutes
7. **Save Model** - Download `trained_model.pt`

### 5. Deploy Trained Model

```bash
# Copy downloaded model to project
cp ~/Downloads/trained_model.pt models/

# Restart backend
cd backend
python main.py
```

Expected output:
```
✓ Model loaded successfully
```

## 🔍 Troubleshooting

### Backend Issues

**Problem:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
# Ensure virtual environment is activated
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

---

**Problem:** `espeak-ng not found`

**Solution:**
```bash
# Windows (as Administrator):
choco install espeak-ng

# macOS:
brew install espeak

# Linux:
sudo apt-get install espeak-ng

# Verify installation:
espeak-ng --version
```

---

**Problem:** Backend starts but model not loaded

**Solution:**
- This is expected before training
- Model loading will succeed after training step
- Backend still works, but returns placeholder scores

---

### Frontend Issues

**Problem:** `npm install` fails

**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

---

**Problem:** Port 3000 already in use

**Solution:**
```bash
# Option 1: Kill process using port 3000
# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:3000 | xargs kill

# Option 2: Use different port
npm run dev -- --port 3001
```

---

**Problem:** CORS errors in browser console

**Solution:**
- Ensure backend is running
- Check backend CORS settings in `main.py`
- Frontend should use port 3000 (configured in CORS origins)

---

### Training Issues

**Problem:** Google Colab disconnects during training

**Solution:**
```bash
# In Colab, run this cell to prevent timeout:
import time
from IPython.display import Javascript

def keep_alive():
    while True:
        display(Javascript('google.colab.output.setIframeHeight(0, true, {maxHeight: 300})'))
        time.sleep(60)

# Run in background
import threading
threading.Thread(target=keep_alive, daemon=True).start()
```

---

**Problem:** CUDA out of memory

**Solution:**
```python
# Reduce batch size in training cell
batch_size = 16  # Instead of 32
```

---

**Problem:** Model file corrupted during download

**Solution:**
```bash
# Verify file size (should be ~500KB - 2MB)
ls -lh models/trained_model.pt

# If size is wrong, re-download from Colab
# Or use direct Drive download
```

## 📊 Performance Expectations

### Development Mode

- **Frontend:** Hot reload in <1 second
- **Backend:** API response <100ms (without ML)
- **Backend with ML:** Analysis ~500ms per audio file

### Production Mode

- **Backend:** Handle 10-50 req/sec (single worker)
- **ML Inference:** ~200-400ms per prediction
- **Frontend:** Load time <2 seconds

## 🔐 Security Checklist

Before production deployment:

- [ ] Change default CORS origins
- [ ] Add authentication middleware
- [ ] Enable HTTPS
- [ ] Sanitize file uploads
- [ ] Rate limit API endpoints
- [ ] Encrypt participant data at rest
- [ ] Add request validation
- [ ] Set up logging and monitoring

## 📚 Next Steps

After successful setup:

1. **Customize UI** - Edit React components in `frontend/src/components/`
2. **Add Words** - Modify word list in `PronunciationTest.tsx`
3. **Collect Real Data** - Have participants use the system
4. **Train Production Model** - Use Colab with full dataset
5. **Deploy** - Follow deployment guide in README.md

## 🆘 Getting Help

If you encounter issues not covered here:

1. Check `ml_colab/ai_training_instructions.txt`
2. Review API docs: http://localhost:8000/docs
3. Search error messages in GitHub issues
4. Check package documentation:
   - FastAPI: https://fastapi.tiangolo.com
   - React: https://react.dev
   - Material UI: https://mui.com

## ✅ Setup Complete!

If all steps succeeded, you now have:

✅ Backend running at http://localhost:8000  
✅ Frontend running at http://localhost:3000  
✅ Data directory ready for participant recordings  
✅ Training notebook ready in Google Colab  
✅ Full development environment configured  

**You're ready to start collecting pronunciation data! 🎉**

---

*Last updated: 2025*
