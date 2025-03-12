# Local Kokoro TTS API

A local API service for Kokoro v1.1 text-to-speech generation.

## Features

- Generate high-quality text-to-speech using Kokoro v1.1 locally
- Simple REST API interface
- Support for multiple voices and languages
- Adjustable speech parameters (speed, pitch, etc.)

## Quick Start

### Linux/macOS

```bash
git clone https://github.com/altommo/local-kokoro-tts.git
cd local-kokoro-tts
chmod +x setup_and_run.sh
./setup_and_run.sh
```

### Windows

```bash
git clone https://github.com/altommo/local-kokoro-tts.git
cd local-kokoro-tts
setup_and_run.bat
```

## Manual Installation with Conda

```bash
# Clone the repository
git clone https://github.com/altommo/local-kokoro-tts.git
cd local-kokoro-tts

# Create and activate Conda environment
conda env create -f environment.yml
conda activate kokoro-tts

# Download Kokoro model
python download_model.py
```

If you don't have Conda installed, you can download it from [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html).

## Alternative Installation with pip

```bash
# Clone the repository
git clone https://github.com/altommo/local-kokoro-tts.git
cd local-kokoro-tts

# Install dependencies
pip install -r requirements.txt

# Download Kokoro model
python download_model.py
```

## Usage

```bash
# Make sure the conda environment is activated (if using Conda)
conda activate kokoro-tts

# Start the API server
python app.py
```

Once the server is running, you can use the API at http://localhost:8000

## Using the Command-line Client

List available voices:
```bash
# With Conda
conda run -n kokoro-tts python client.py voices

# Without Conda
python client.py voices
```

Generate speech:
```bash
# With Conda
conda run -n kokoro-tts python client.py generate --text "Hello, this is Kokoro text to speech!"

# Without Conda
python client.py generate --text "Hello, this is Kokoro text to speech!"
```

## API Documentation

Visit http://localhost:8000/docs for interactive API documentation.

## Docker Usage

```bash
# Build and start the Docker container
docker-compose up -d
```

## License

MIT