# Local Kokoro TTS API

A local API service for Kokoro v1.1 text-to-speech generation.

## Features

- Generate high-quality text-to-speech using Kokoro v1.1 locally
- Simple REST API interface
- Support for multiple voices and languages
- Adjustable speech parameters (speed, pitch, etc.)

## Installation

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
# Start the API server
python app.py
```

Once the server is running, you can use the API at http://localhost:8000

## API Documentation

Visit http://localhost:8000/docs for interactive API documentation.

## License

MIT
