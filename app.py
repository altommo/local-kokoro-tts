#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException, BackgroundTasks, Query, Form, UploadFile, File
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import io
import os
import scipy.io.wavfile
import numpy as np
import time
from typing import List, Optional
from pydantic import BaseModel
from pathlib import Path

from model import KokoroTTS

app = FastAPI(
    title="Kokoro TTS API",
    description="A local API for Kokoro v1.1 text-to-speech generation",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model instance
tts_model = None

class TTSRequest(BaseModel):
    text: str
    voice_id: str = "en_female_1"
    speed: float = 1.0
    pitch: float = 0.0
    sample_rate: int = 24000

class BatchTTSRequest(BaseModel):
    items: List[TTSRequest]
    
class VoiceInfo(BaseModel):
    id: str
    name: str
    language: str

@app.on_event("startup")
async def startup_event():
    global tts_model
    model_dir = Path("models/kokoro-v1.1")
    
    # Check if model exists, if not suggest downloading
    if not model_dir.exists():
        print(f"Model not found at {model_dir}. Please run 'python download_model.py' first.")
    else:
        tts_model = KokoroTTS(model_path=str(model_dir))

@app.get("/")
def read_root():
    return {"message": "Kokoro TTS API is running", "status": "ok"}

@app.get("/health")
def health_check():
    global tts_model
    if tts_model is None:
        return {"status": "error", "message": "TTS model not loaded"}
    return {"status": "ok", "message": "TTS model is loaded and ready"}

@app.get("/voices", response_model=List[VoiceInfo])
def get_voices():
    global tts_model
    if tts_model is None:
        raise HTTPException(status_code=503, detail="TTS model not loaded yet")
    return tts_model.get_available_voices()

@app.post("/tts")
async def text_to_speech(request: TTSRequest):
    global tts_model
    if tts_model is None:
        raise HTTPException(status_code=503, detail="TTS model not loaded yet")
    
    try:
        # Generate speech
        start_time = time.time()
        audio, sample_rate = tts_model.generate_speech(
            text=request.text,
            voice_id=request.voice_id,
            speed=request.speed,
            pitch=request.pitch,
            sample_rate=request.sample_rate
        )
        generation_time = time.time() - start_time
        
        # Convert to WAV format
        wav_io = io.BytesIO()
        scipy.io.wavfile.write(wav_io, sample_rate, (audio * 32767).astype(np.int16))
        wav_io.seek(0)
        
        # Return audio file
        return StreamingResponse(
            wav_io, 
            media_type="audio/wav",
            headers={
                "X-Generation-Time": f"{generation_time:.2f}s",
                "Content-Disposition": "attachment; filename=speech.wav"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tts/form")
async def text_to_speech_form(
    text: str = Form(...),
    voice_id: str = Form("en_female_1"),
    speed: float = Form(1.0),
    pitch: float = Form(0.0),
    sample_rate: int = Form(24000)
):
    request = TTSRequest(
        text=text,
        voice_id=voice_id,
        speed=speed,
        pitch=pitch,
        sample_rate=sample_rate
    )
    return await text_to_speech(request)

@app.post("/tts/batch")
async def batch_tts(request: BatchTTSRequest, background_tasks: BackgroundTasks):
    global tts_model
    if tts_model is None:
        raise HTTPException(status_code=503, detail="TTS model not loaded yet")
    
    if len(request.items) == 0:
        raise HTTPException(status_code=400, detail="Batch request must contain at least one item")
    
    # For simplicity, we'll just return a success message
    # In a real implementation, you would process these in the background
    # and provide a way to retrieve the results
    return {"status": "processing", "message": f"Processing {len(request.items)} items in batch"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
