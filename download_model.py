#!/usr/bin/env python3

import os
import sys
import requests
import zipfile
import argparse
from pathlib import Path

DEFAULT_MODEL_DIR = "models"
KOKORO_MODEL_URL = "https://huggingface.co/spaces/kokoro-tts/models/resolve/main/kokoro-v1.1.zip"

def download_file(url, destination):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total_size = int(r.headers.get('content-length', 0))
        downloaded = 0
        with open(destination, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                downloaded += len(chunk)
                f.write(chunk)
                sys.stdout.write(f"\rDownloading... {downloaded / total_size * 100:.1f}%")
                sys.stdout.flush()
    print("\nDownload complete!")

def extract_zip(zip_path, extract_to):
    print(f"Extracting to {extract_to}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print("Extraction complete!")

def main():
    parser = argparse.ArgumentParser(description="Download Kokoro TTS model")
    parser.add_argument(
        "--model-dir", 
        type=str, 
        default=DEFAULT_MODEL_DIR,
        help=f"Directory to save the model (default: {DEFAULT_MODEL_DIR})"
    )
    args = parser.parse_args()
    
    model_dir = Path(args.model_dir)
    model_dir.mkdir(exist_ok=True, parents=True)
    
    zip_path = model_dir / "kokoro-v1.1.zip"
    
    print(f"Downloading Kokoro v1.1 model from {KOKORO_MODEL_URL}...")
    download_file(KOKORO_MODEL_URL, zip_path)
    
    extract_zip(zip_path, model_dir)
    
    # Remove the zip file after extraction
    os.remove(zip_path)
    print(f"Model downloaded and extracted to {model_dir}")
    print("You can now run the API server with: python app.py")

if __name__ == "__main__":
    main()
