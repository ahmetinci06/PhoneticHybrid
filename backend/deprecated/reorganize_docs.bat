@echo off
REM Documentation Reorganization Script
REM This script organizes all documentation into the docs/ folder structure

echo ========================================
echo PhoneticHybrid Documentation Reorganization
echo ========================================
echo.

REM Create directory structure
echo Creating directory structure...
mkdir docs\setup 2>nul
mkdir docs\guides 2>nul
mkdir docs\architecture 2>nul
mkdir docs\azure 2>nul
mkdir docs\deployment 2>nul
mkdir docs\deprecated 2>nul
mkdir backend\deprecated\ml_colab 2>nul

echo.
echo Moving setup documentation...
move /Y QUICK_START.md docs\setup\ 2>nul
move /Y SETUP_GUIDE.md docs\setup\ 2>nul
move /Y INSTALLATION_SUCCESS.md docs\setup\ 2>nul
move /Y ESPEAK_WINDOWS_INSTALL.md docs\setup\ 2>nul
move /Y PYTHON_VERSION_FIX.md docs\setup\ 2>nul

echo Moving user guides...
move /Y PHONEME_FEATURE.md docs\guides\ 2>nul
move /Y PHONEME_QUICK_START.txt docs\guides\ 2>nul
move /Y PHONEME_VERIFICATION.md docs\guides\ 2>nul
move /Y PRONUNCIATION_ANALYSIS_GUIDE.md docs\guides\ 2>nul
move /Y ANALYSIS_QUICK_REF.txt docs\guides\ 2>nul
move /Y REVIEW_INTERFACE_GUIDE.md docs\guides\ 2>nul
move /Y VISUAL_GUIDE.md docs\guides\ 2>nul

echo Moving architecture documentation...
move /Y PROJECT_STRUCTURE.md docs\architecture\ 2>nul
move /Y SYSTEM_OVERVIEW.md docs\architecture\ 2>nul
move /Y IMPLEMENTATION_SUMMARY.md docs\architecture\ 2>nul

echo Moving Azure documentation...
move /Y AZURE_INTEGRATION_SUMMARY.md docs\azure\ 2>nul

echo Moving deployment documentation...
move /Y DEPLOYMENT.md docs\deployment\ 2>nul

echo Moving deprecated ML training documentation...
move /Y ML_TRAINING_GUIDE.md docs\deprecated\ 2>nul
move /Y ML_QUICK_START.txt docs\deprecated\ 2>nul

echo Moving ml_colab to deprecated...
xcopy /E /I /Y ml_colab backend\deprecated\ml_colab
rmdir /S /Q ml_colab 2>nul

echo.
echo ========================================
echo Reorganization Complete!
echo ========================================
echo.
echo New structure:
echo   docs/
echo     setup/         - Installation guides
echo     guides/        - User guides
echo     architecture/  - System architecture
echo     azure/         - Azure integration
echo     deployment/    - Deployment guides
echo     deprecated/    - Old ML training docs
echo.
echo   backend/deprecated/
echo     ml_colab/      - Archived Colab notebooks
echo.
echo Root directory now contains only:
echo   - README.md
echo   - LICENSE
echo   - CONTRIBUTING.md
echo.
pause
