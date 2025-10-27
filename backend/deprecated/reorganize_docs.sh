#!/bin/bash
# Documentation Reorganization Script
# This script organizes all documentation into the docs/ folder structure

echo "========================================"
echo "PhoneticHybrid Documentation Reorganization"
echo "========================================"
echo ""

# Create directory structure
echo "Creating directory structure..."
mkdir -p docs/setup
mkdir -p docs/guides
mkdir -p docs/architecture
mkdir -p docs/azure
mkdir -p docs/deployment
mkdir -p docs/deprecated
mkdir -p backend/deprecated/ml_colab

echo ""
echo "Moving setup documentation..."
mv -f QUICK_START.md docs/setup/ 2>/dev/null || true
mv -f SETUP_GUIDE.md docs/setup/ 2>/dev/null || true
mv -f INSTALLATION_SUCCESS.md docs/setup/ 2>/dev/null || true
mv -f ESPEAK_WINDOWS_INSTALL.md docs/setup/ 2>/dev/null || true
mv -f PYTHON_VERSION_FIX.md docs/setup/ 2>/dev/null || true

echo "Moving user guides..."
mv -f PHONEME_FEATURE.md docs/guides/ 2>/dev/null || true
mv -f PHONEME_QUICK_START.txt docs/guides/ 2>/dev/null || true
mv -f PHONEME_VERIFICATION.md docs/guides/ 2>/dev/null || true
mv -f PRONUNCIATION_ANALYSIS_GUIDE.md docs/guides/ 2>/dev/null || true
mv -f ANALYSIS_QUICK_REF.txt docs/guides/ 2>/dev/null || true
mv -f REVIEW_INTERFACE_GUIDE.md docs/guides/ 2>/dev/null || true
mv -f VISUAL_GUIDE.md docs/guides/ 2>/dev/null || true

echo "Moving architecture documentation..."
mv -f PROJECT_STRUCTURE.md docs/architecture/ 2>/dev/null || true
mv -f SYSTEM_OVERVIEW.md docs/architecture/ 2>/dev/null || true
mv -f IMPLEMENTATION_SUMMARY.md docs/architecture/ 2>/dev/null || true

echo "Moving Azure documentation..."
mv -f AZURE_INTEGRATION_SUMMARY.md docs/azure/ 2>/dev/null || true

echo "Moving deployment documentation..."
mv -f DEPLOYMENT.md docs/deployment/ 2>/dev/null || true

echo "Moving deprecated ML training documentation..."
mv -f ML_TRAINING_GUIDE.md docs/deprecated/ 2>/dev/null || true
mv -f ML_QUICK_START.txt docs/deprecated/ 2>/dev/null || true

echo "Moving ml_colab to deprecated..."
if [ -d "ml_colab" ]; then
    cp -r ml_colab/* backend/deprecated/ml_colab/
    rm -rf ml_colab
fi

echo ""
echo "========================================"
echo "Reorganization Complete!"
echo "========================================"
echo ""
echo "New structure:"
echo "  docs/"
echo "    setup/         - Installation guides"
echo "    guides/        - User guides"
echo "    architecture/  - System architecture"
echo "    azure/         - Azure integration"
echo "    deployment/    - Deployment guides"
echo "    deprecated/    - Old ML training docs"
echo ""
echo "  backend/deprecated/"
echo "    ml_colab/      - Archived Colab notebooks"
echo ""
echo "Root directory now contains only:"
echo "  - README.md"
echo "  - LICENSE"
echo "  - CONTRIBUTING.md"
echo ""
