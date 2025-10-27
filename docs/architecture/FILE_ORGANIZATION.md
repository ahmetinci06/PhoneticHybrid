# Project File Organization

## Overview

This document explains the organized file structure of the PhoneticHybrid project.

## Root Directory (Clean & Minimal)

The root directory contains only essential project files:

```
PhoneticHybrid/
├── README.md              # Main project overview
├── LICENSE                # MIT License
├── CONTRIBUTING.md        # Contribution guidelines
├── .gitignore            # Git ignore patterns
├── .gitattributes        # Git attributes
├── start_dev.bat         # Windows development startup
├── start_dev.sh          # Unix development startup
├── docs/                 # 📚 All documentation
├── backend/              # Backend application
├── frontend/             # Frontend application
├── data/                 # Participant data
└── models/               # ML models (if any)
```

## Documentation Structure (`docs/`)

All documentation is organized in the `docs/` folder with clear categorization:

### Setup Documentation (`docs/setup/`)
Installation and configuration guides:
- `QUICK_START.md` - 5-minute quick start
- `SETUP_GUIDE.md` - Complete setup guide
- `INSTALLATION_SUCCESS.md` - Verification guide
- `ESPEAK_WINDOWS_INSTALL.md` - Windows eSpeak setup
- `PYTHON_VERSION_FIX.md` - Python compatibility

### User Guides (`docs/guides/`)
End-user and developer guides:
- `PHONEME_FEATURE.md` - Phoneme system guide
- `PHONEME_QUICK_START.txt` - Quick phoneme setup
- `PHONEME_VERIFICATION.md` - Testing phonemes
- `PRONUNCIATION_ANALYSIS_GUIDE.md` - Analysis API guide
- `ANALYSIS_QUICK_REF.txt` - Quick API reference
- `REVIEW_INTERFACE_GUIDE.md` - Review UI guide
- `VISUAL_GUIDE.md` - Screenshots and walkthroughs

### Architecture (`docs/architecture/`)
Technical architecture and design:
- `PROJECT_STRUCTURE.md` - Codebase structure
- `SYSTEM_OVERVIEW.md` - System architecture
- `IMPLEMENTATION_SUMMARY.md` - Implementation details
- `FILE_ORGANIZATION.md` - This file

### Azure Integration (`docs/azure/`)
Azure Speech Services documentation:
- `AZURE_INTEGRATION_SUMMARY.md` - Complete Azure guide

### Deployment (`docs/deployment/`)
Production deployment guides:
- `DEPLOYMENT.md` - Deployment instructions

### Deprecated (`docs/deprecated/`)
Archived ML training documentation:
- `README.md` - Deprecation notice
- `ML_TRAINING_GUIDE.md` - Old ML training guide
- `ML_QUICK_START.txt` - Old ML quick start

## Backend Structure (`backend/`)

```
backend/
├── main.py                # FastAPI application
├── inference.py           # Pronunciation analysis
├── azure_config.py        # Azure configuration
├── phoneme_service.py     # Phoneme generation
├── review_api.py          # Review interface API
├── ml_scorer.py           # ML scoring (legacy)
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── .env                  # Environment config (not in git)
├── temp_audio/           # Temporary audio storage
├── deprecated/           # 🗄️ Archived files
│   ├── README.md
│   ├── train_ml_model.py
│   ├── prepare_training_data.py
│   ├── test_analysis.py
│   └── ml_colab/         # Archived Colab notebooks
│       ├── training_notebook.ipynb
│       ├── pronunciation_scoring_training.ipynb
│       ├── training_environment_setup.txt
│       └── ai_training_instructions.txt
└── venv/                 # Python virtual environment (not in git)
```

## Frontend Structure (`frontend/`)

```
frontend/
├── src/
│   ├── components/       # React components
│   │   ├── Welcome.tsx
│   │   ├── ConsentForm.tsx
│   │   ├── OrthodonticSurvey.tsx
│   │   ├── PronunciationTest.tsx
│   │   ├── PhonemePreview.tsx
│   │   ├── FinishScreen.tsx
│   │   └── LikertScale.tsx
│   ├── pages/
│   │   └── ReviewPage.tsx
│   ├── App.tsx
│   └── main.tsx
├── package.json
├── vite.config.ts
└── node_modules/         # Dependencies (not in git)
```

## Data Directory (`data/`)

Participant data storage:

```
data/
└── participant_<uuid>/
    ├── info.json         # Participant information
    ├── survey.json       # Survey responses
    └── kelimeler/        # Audio recordings
        ├── 01_word.wav
        ├── 01_word_result.json
        └── ...
```

## Organization Benefits

### 1. **Clean Root Directory**
- Easy to navigate
- Only essential files visible
- Professional appearance

### 2. **Categorized Documentation**
- Easy to find relevant docs
- Logical organization
- Clear separation of concerns

### 3. **Deprecated Code Archive**
- Old code preserved for reference
- Clearly marked as deprecated
- Doesn't clutter active codebase

### 4. **Consistent Structure**
- Follows best practices
- Easy for new contributors
- Scalable organization

## Finding Files

### For New Users
Start here: **[Quick Start Guide](../setup/QUICK_START.md)**

### For Azure Setup
Go to: **[Azure Integration](../azure/AZURE_INTEGRATION_SUMMARY.md)**

### For API Reference
See: **[Pronunciation Analysis Guide](../guides/PRONUNCIATION_ANALYSIS_GUIDE.md)**

### For Architecture
Read: **[System Overview](SYSTEM_OVERVIEW.md)**

## File Naming Conventions

- **UPPERCASE.md** - Important documentation files
- **lowercase.py** - Python source files
- **PascalCase.tsx** - React components
- **kebab-case.json** - Configuration files

## What's Not in Git

The following are ignored by `.gitignore`:

- `node_modules/` - Frontend dependencies
- `venv/` - Python virtual environment
- `.env` - Environment variables (secrets)
- `temp_audio/` - Temporary audio files
- `data/participant_*/` - User data
- `__pycache__/` - Python cache
- `*.pyc` - Compiled Python files
- `.DS_Store` - macOS system files

## Maintaining Organization

When adding new files:

1. **Documentation** → Add to appropriate `docs/` subfolder
2. **Backend code** → Add to `backend/`
3. **Frontend code** → Add to `frontend/src/`
4. **Deprecated code** → Move to `backend/deprecated/`

Update this document if you:
- Add new documentation categories
- Change folder structure
- Archive more components

---

**Last Updated:** October 2025
