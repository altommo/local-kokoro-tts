#!/usr/bin/env python3

import requests
import argparse
import json
import os
from pathlib import Path

DEFAULT_API_URL = "http://localhost:8000"

def list_voices(api_url):
    response = requests.get(f"{api_url}/voices")
    if response.status_code == 200:
        voices = response.json()
        print("Available voices:")
        for voice in voices:
            print(f"  - {voice['id']}: {voice['name']} ({voice['language']})")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def generate_speech(api_url, text, voice_id, speed, pitch, sample_rate, output_file):
    data = {
        "text": text,
        "voice_id": voice_id,
        "speed": speed,
        "pitch": pitch,
        "sample_rate": sample_rate
    }
    
    print(f"Generating speech for text: '{text[:50]}{'...' if len(text) > 50 else ''}'")
    response = requests.post(f"{api_url}/tts", json=data)
    
    if response.status_code == 200:
        output_path = Path(output_file)
        output_path.parent.mkdir(exist_ok=True, parents=True)
        
        with open(output_path, "wb") as f:
            f.write(response.content)
        
        generation_time = response.headers.get("X-Generation-Time", "unknown")
        print(f"Speech generated in {generation_time}")
        print(f"Audio saved to {output_path}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def main():
    parser = argparse.ArgumentParser(description="Kokoro TTS client")
    parser.add_argument(
        "--api-url", 
        type=str, 
        default=DEFAULT_API_URL,
        help=f"API server URL (default: {DEFAULT_API_URL})"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # 'voices' command
    voices_parser = subparsers.add_parser("voices", help="List available voices")
    
    # 'generate' command
    generate_parser = subparsers.add_parser("generate", help="Generate speech from text")
    generate_parser.add_argument("--text", type=str, required=True, help="Text to convert to speech")
    generate_parser.add_argument("--voice", type=str, default="en_female_1", help="Voice ID to use")
    generate_parser.add_argument("--speed", type=float, default=1.0, help="Speech speed factor (0.5-2.0)")
    generate_parser.add_argument("--pitch", type=float, default=0.0, help="Pitch adjustment in semitones (-12 to 12)")
    generate_parser.add_argument("--sample-rate", type=int, default=24000, help="Output sample rate")
    generate_parser.add_argument("--output", type=str, default="output.wav", help="Output file path")
    
    args = parser.parse_args()
    
    if args.command == "voices":
        list_voices(args.api_url)
    elif args.command == "generate":
        generate_speech(
            api_url=args.api_url,
            text=args.text,
            voice_id=args.voice,
            speed=args.speed,
            pitch=args.pitch,
            sample_rate=args.sample_rate,
            output_file=args.output
        )
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
