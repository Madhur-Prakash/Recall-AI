from fastapi import APIRouter, UploadFile, File, HTTPException, status
import numpy as np
import soundfile as sf
from io import BytesIO
from voice_config.voice import process_with_server, transcribe_audio_direct
from recall_ai.helpers.utils import setup_logging

voice = APIRouter()
logger = setup_logging()

@voice.post("/voice_input", status_code=200)
async def voice_input(file: UploadFile = File(...)):
    try:
        # Read audio file sent by frontend
        audio_bytes = await file.read()
        
        # Log file info
        logger.info(f"Received audio file: {file.filename}, content_type: {file.content_type}, size: {len(audio_bytes)} bytes")
        
        # Read audio data - soundfile handles MP3, WAV, FLAC, etc.
        try:
            audio_np, samplerate = sf.read(BytesIO(audio_bytes), dtype="float32")
            logger.info(f"Audio loaded successfully - shape: {audio_np.shape}, sample_rate: {samplerate}")
        except Exception as e:
            logger.error(f"Audio reading error: {e}")
            return {"status": "error", "message": "Could not read audio data. Please ensure it's a valid audio file."}
        
        # Ensure audio is not empty
        if len(audio_np) == 0:
            return {"status": "error", "message": "Audio file is empty or corrupted."}
        
        # Transcribe
        transcription = transcribe_audio_direct(audio_np)

        if not transcription:
            return {"status": "error", "message": "Could not understand speech."}

        # Call secondary server (e.g., GPT-like response)
        server_response = await process_with_server(transcription)

        if not server_response:
            return {"status": "error", "message": "Could not get server response."}

        return {
            "status": "success",
            "transcription": transcription,
            "response": server_response
        }

    except Exception as e:
        logger.error(f"Voice input error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")