@echo off
REM Backend Cleanup Script
REM Moves deprecated ML training files to backend/deprecated/

echo ========================================
echo Backend Repository Cleanup
echo ========================================
echo.
echo Moving deprecated ML training files...
echo.

REM Move old ML files to deprecated
move /Y backend\train_ml_model.py backend\deprecated\ 2>nul
move /Y backend\prepare_training_data.py backend\deprecated\ 2>nul
move /Y backend\test_analysis.py backend\deprecated\ 2>nul
move /Y backend\ml_scorer.py backend\deprecated\ 2>nul

echo.
echo ========================================
echo Cleanup Complete!
echo ========================================
echo.
echo Moved to backend/deprecated/:
echo   - train_ml_model.py
echo   - prepare_training_data.py
echo   - test_analysis.py
echo   - ml_scorer.py
echo.
echo Your backend/ directory is now clean!
echo.
echo Only active files remain:
echo   - main.py (FastAPI app)
echo   - inference.py (Azure + phoneme analysis)
echo   - azure_config.py (Azure configuration)
echo   - phoneme_service.py (Phoneme generation)
echo   - review_api.py (Review interface)
echo   - requirements.txt
echo   - .env.example
echo.
pause
