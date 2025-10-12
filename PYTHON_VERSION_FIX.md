# Python Version Compatibility Fix

## Problem
Python 3.13 is too new - many scientific packages (numpy, scipy, librosa) don't have pre-built wheels yet.

## Solution: Use Python 3.10 or 3.11

### Option 1: Install Python 3.11 (Recommended)

1. **Download Python 3.11:**
   - Go to: https://www.python.org/downloads/
   - Download Python 3.11.x (latest 3.11 version)
   - Install with "Add to PATH" checked

2. **Recreate Virtual Environment:**
   ```bash
   cd backend
   
   # Remove old venv
   rm -rf venv
   
   # Create new venv with Python 3.11
   py -3.11 -m venv venv
   
   # Activate
   venv\Scripts\activate
   
   # Upgrade pip
   python -m pip install --upgrade pip setuptools wheel
   
   # Install requirements
   pip install -r requirements.txt
   ```

### Option 2: Use Conda (Alternative)

If you have Anaconda/Miniconda:

```bash
cd backend

# Create conda environment with Python 3.11
conda create -n phoneizer python=3.11 -y

# Activate
conda activate phoneizer

# Install requirements
pip install -r requirements.txt
```

### Option 3: Simplified Requirements (Quick Fix)

If you want to test quickly without ML features:

```bash
cd backend

# Install minimal dependencies first
pip install fastapi uvicorn[standard] python-multipart pydantic

# Then try ML packages one by one
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install librosa soundfile
```

## Verification

After installation, verify:

```bash
python --version  # Should show 3.10.x or 3.11.x
python -c "import torch; print(torch.__version__)"
python -c "import librosa; print(librosa.__version__)"
python -c "import fastapi; print(fastapi.__version__)"
```

## Why This Happens

- Python 3.13 was released very recently (October 2024)
- Scientific packages need time to compile wheels for new Python versions
- numpy, scipy, and librosa require C extensions that must be rebuilt
- Python 3.11 has full ecosystem support

## Recommended Action

**Use Python 3.11** - it's stable, fast, and all packages work perfectly.
