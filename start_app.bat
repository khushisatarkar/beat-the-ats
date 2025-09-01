@echo off
echo ========================================
echo    Resume Scanner - Starting Up
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Python found! Checking version...
python --version

echo.
echo Installing/updating dependencies...
pip install -r requirements.txt

echo.
echo Downloading spaCy model...
python -m spacy download en_core_web_sm

echo.
echo ========================================
echo    Starting Resume Scanner...
echo ========================================
echo.
echo The application will open at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
