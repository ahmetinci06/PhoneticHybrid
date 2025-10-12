# Quick Start Guide ⚡

Get PhoneticHybrid running in 5 minutes!

## Prerequisites

✅ Node.js 18+  
✅ Python 3.10+  
✅ Git

## Installation (One-time Setup)

### 1. Backend Setup (3 minutes)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# OR Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Frontend Setup (2 minutes)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install
```

## Running the Application

### Option A: Automated Start (Recommended)

**Windows:**
```bash
# Double-click or run:
start_dev.bat
```

**macOS/Linux:**
```bash
# Make executable first time:
chmod +x start_dev.sh

# Run:
./start_dev.sh
```

This will start both servers automatically!

### Option B: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
# Activate venv first (see above)
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## Access the App

🌐 **Frontend:** http://localhost:3000  
🔧 **Backend API:** http://localhost:8000  
📚 **API Docs:** http://localhost:8000/docs

## First Run Experience

When you first start:

1. **Backend** will show:
   ```
   ⚠ Model not found. Train the model first using the Colab notebook.
   ```
   This is normal! The app works without the ML model for data collection.

2. **Frontend** will display the welcome screen

3. Test the flow:
   - Click "Başlamak İçin Tıklayın"
   - Fill out the consent form
   - Complete the survey
   - Record at least one test word
   - Check `data/` folder for participant data

## Next Steps

### For Development:
- Edit components in `frontend/src/components/`
- Edit API in `backend/main.py`
- Changes auto-reload in dev mode

### For ML Training:
1. Collect data from participants (at least 50 recommended)
2. Follow `ml_colab/ai_training_instructions.txt`
3. Upload data to Google Drive
4. Run training notebook in Colab
5. Download and deploy model

## Troubleshooting

**Port Already in Use:**
```bash
# Backend (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Frontend (Windows)
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

**ModuleNotFoundError:**
```bash
# Make sure venv is activated
cd backend
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

**npm install fails:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## Common Commands

```bash
# Backend
cd backend
python main.py              # Start server
pip list                    # Show installed packages
pytest                      # Run tests

# Frontend
cd frontend
npm run dev                 # Start dev server
npm run build               # Build for production
npm run preview             # Preview production build

# Project
git status                  # Check changes
git add .                   # Stage changes
git commit -m "message"     # Commit changes
```

## Directory Overview

```
phoneizer/
├── frontend/          → React app (port 3000)
├── backend/           → FastAPI server (port 8000)
├── ml_colab/          → Training notebook
├── data/              → Participant recordings
└── models/            → Trained ML model
```

## What to Do Next

1. ✅ **Test the App** - Complete one full recording session
2. 📖 **Read Documentation** - Check `README.md` and `SETUP_GUIDE.md`
3. 🎨 **Customize UI** - Edit components to match your needs
4. 📊 **Collect Data** - Share with participants
5. 🤖 **Train Model** - Once you have enough data

## Need Help?

- 📘 **Full Setup:** `SETUP_GUIDE.md`
- 🏗️ **Architecture:** `README.md`
- 🎓 **ML Training:** `ml_colab/ai_training_instructions.txt`
- 🚀 **Deployment:** `DEPLOYMENT.md`
- 🤝 **Contributing:** `CONTRIBUTING.md`

---

**Happy coding! 🎉**
