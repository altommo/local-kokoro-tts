#!/bin/bash

# Exit on error
set -e

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "Conda is not installed. Please install Miniconda or Anaconda first."
    echo "Visit: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

# Create and activate the conda environment
echo "Setting up Conda environment..."
if conda env list | grep -q "kokoro-tts"; then
    echo "Environment already exists, updating..."
    conda env update -f environment.yml
else
    echo "Creating new environment..."
    conda env create -f environment.yml
fi

# Activate the environment
eval "$(conda shell.bash hook)"
conda activate kokoro-tts

# Check if model exists, if not download it
if [ ! -d "models/kokoro-v1.1" ]; then
    echo "Downloading Kokoro model..."
    python download_model.py
else
    echo "Model already downloaded."
fi

# Start the API server
echo "Starting Kokoro TTS API server..."
python app.py