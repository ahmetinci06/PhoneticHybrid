# Documentation Reorganization Guide

This guide explains the new organized structure for PhoneticHybrid documentation and how to apply it.

## 📋 What's Being Reorganized

### Documentation Files (`.md` and `.txt`)
All scattered documentation files in the root directory are being moved to a structured `docs/` folder.

### ML Training Materials
The deprecated ML training notebooks and related files are being moved to `backend/deprecated/ml_colab/`.

## 🎯 New Structure

```
PhoneticHybrid/
├── README.md                    # Main project README (STAYS)
├── LICENSE                      # License file (STAYS)
├── CONTRIBUTING.md              # Contribution guidelines (STAYS)
├── .gitignore                   # Git ignore file (STAYS)
│
├── docs/                        # 📚 ALL DOCUMENTATION (NEW)
│   ├── README.md               # Documentation index
│   │
│   ├── setup/                  # Installation & Setup
│   │   ├── QUICK_START.md
│   │   ├── SETUP_GUIDE.md
│   │   ├── INSTALLATION_SUCCESS.md
│   │   ├── ESPEAK_WINDOWS_INSTALL.md
│   │   └── PYTHON_VERSION_FIX.md
│   │
│   ├── guides/                 # User Guides
│   │   ├── PHONEME_FEATURE.md
│   │   ├── PHONEME_QUICK_START.txt
│   │   ├── PHONEME_VERIFICATION.md
│   │   ├── PRONUNCIATION_ANALYSIS_GUIDE.md
│   │   ├── ANALYSIS_QUICK_REF.txt
│   │   ├── REVIEW_INTERFACE_GUIDE.md
│   │   └── VISUAL_GUIDE.md
│   │
│   ├── architecture/           # Architecture & Implementation
│   │   ├── PROJECT_STRUCTURE.md
│   │   ├── SYSTEM_OVERVIEW.md
│   │   └── IMPLEMENTATION_SUMMARY.md
│   │
│   ├── azure/                  # Azure Integration
│   │   └── AZURE_INTEGRATION_SUMMARY.md
│   │
│   ├── deployment/             # Deployment
│   │   └── DEPLOYMENT.md
│   │
│   └── deprecated/             # Old ML Training Docs
│       ├── README.md
│       ├── ML_TRAINING_GUIDE.md
│       └── ML_QUICK_START.txt
│
├── backend/
│   ├── deprecated/             # Archived Code
│   │   ├── README.md
│   │   ├── train_ml_model.py
│   │   ├── prepare_training_data.py
│   │   ├── test_analysis.py
│   │   └── ml_colab/          # 📦 MOVED FROM ROOT
│   │       ├── training_notebook.ipynb
│   │       ├── pronunciation_scoring_training.ipynb
│   │       ├── training_environment_setup.txt
│   │       └── ai_training_instructions.txt
│   │
│   └── [other backend files...]
│
├── frontend/
└── [other root files...]
```

## 🚀 How to Apply

### Option 1: Automated Script (Recommended)

**Windows:**
```bash
reorganize_docs.bat
```

**Linux/Mac:**
```bash
chmod +x reorganize_docs.sh
./reorganize_docs.sh
```

### Option 2: Manual Reorganization

Follow this checklist:

#### 1. Create Directory Structure
```bash
mkdir -p docs/setup
mkdir -p docs/guides
mkdir -p docs/architecture
mkdir -p docs/azure
mkdir -p docs/deployment
mkdir -p docs/deprecated
mkdir -p backend/deprecated/ml_colab
```

#### 2. Move Setup Documentation
```bash
mv QUICK_START.md docs/setup/
mv SETUP_GUIDE.md docs/setup/
mv INSTALLATION_SUCCESS.md docs/setup/
mv ESPEAK_WINDOWS_INSTALL.md docs/setup/
mv PYTHON_VERSION_FIX.md docs/setup/
```

#### 3. Move User Guides
```bash
mv PHONEME_FEATURE.md docs/guides/
mv PHONEME_QUICK_START.txt docs/guides/
mv PHONEME_VERIFICATION.md docs/guides/
mv PRONUNCIATION_ANALYSIS_GUIDE.md docs/guides/
mv ANALYSIS_QUICK_REF.txt docs/guides/
mv REVIEW_INTERFACE_GUIDE.md docs/guides/
mv VISUAL_GUIDE.md docs/guides/
```

#### 4. Move Architecture Documentation
```bash
mv PROJECT_STRUCTURE.md docs/architecture/
mv SYSTEM_OVERVIEW.md docs/architecture/
mv IMPLEMENTATION_SUMMARY.md docs/architecture/
```

#### 5. Move Azure Documentation
```bash
mv AZURE_INTEGRATION_SUMMARY.md docs/azure/
```

#### 6. Move Deployment Documentation
```bash
mv DEPLOYMENT.md docs/deployment/
```

#### 7. Move Deprecated Documentation
```bash
mv ML_TRAINING_GUIDE.md docs/deprecated/
mv ML_QUICK_START.txt docs/deprecated/
```

#### 8. Move ml_colab Folder
```bash
mv ml_colab backend/deprecated/
```

## ✅ Verification

After reorganization, your root directory should only contain:

```
PhoneticHybrid/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── .gitignore
├── .gitattributes
├── start_dev.bat
├── start_dev.sh
├── docs/              # All documentation here
├── backend/
├── frontend/
├── data/
└── models/
```

Check that:
- ✅ Root is clean (only essential files)
- ✅ All docs in `docs/` folder
- ✅ `ml_colab/` moved to `backend/deprecated/ml_colab/`
- ✅ Documentation is accessible via `docs/README.md`

## 📝 Update References

After moving files, update any references in:

1. **README.md** - Update documentation links
2. **Code comments** - Fix any hardcoded paths
3. **CI/CD scripts** - Update documentation paths

Example:
```markdown
<!-- Before -->
See [Setup Guide](SETUP_GUIDE.md)

<!-- After -->
See [Setup Guide](docs/setup/SETUP_GUIDE.md)
```

## 🔍 Finding Documentation

After reorganization, use the **Documentation Index**:

👉 **[docs/README.md](docs/README.md)** - Complete documentation index

Or navigate directly:
- **Getting Started:** `docs/setup/QUICK_START.md`
- **Azure Setup:** `docs/azure/AZURE_INTEGRATION_SUMMARY.md`
- **API Guide:** `docs/guides/PRONUNCIATION_ANALYSIS_GUIDE.md`
- **Architecture:** `docs/architecture/SYSTEM_OVERVIEW.md`

## 🗑️ What Can Be Deleted (Optional)

After reorganization, you can optionally delete:
- `reorganize_docs.bat`
- `reorganize_docs.sh`
- `REORGANIZATION_GUIDE.md` (this file)

## 🆘 Troubleshooting

**Files not found after moving?**
- Check `docs/` subfolders
- Verify the move completed successfully
- Look in `backend/deprecated/` for ML-related files

**Links broken in documentation?**
- Update relative paths in markdown files
- Use documentation index in `docs/README.md`

**Git shows too many changes?**
- This is normal - files are being moved
- Commit with message: "docs: reorganize documentation structure"

---

**Ready to reorganize?** Run the script or follow the manual steps above!
