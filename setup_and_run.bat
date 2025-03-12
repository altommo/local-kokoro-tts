@echo off
SETLOCAL EnableDelayedExpansion

REM Check if conda is installed
where conda >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Conda is not installed. Please install Miniconda or Anaconda first.
    echo Visit: https://docs.conda.io/en/latest/miniconda.html
    exit /b 1
)

REM Create and activate the conda environment
echo Setting up Conda environment...
conda env list | findstr /C:"kokoro-tts" >nul
IF %ERRORLEVEL% EQU 0 (
    echo Environment already exists, updating...
    conda env update -f environment.yml
) ELSE (
    echo Creating new environment...
    conda env create -f environment.yml
)

REM Activate the environment
call conda activate kokoro-tts

REM Check if model exists, if not download it
IF NOT EXIST models\kokoro-v1.1 (
    echo Downloading Kokoro model...
    python download_model.py
) ELSE (
    echo Model already downloaded.
)

REM Start the API server
echo Starting Kokoro TTS API server...
python app.py