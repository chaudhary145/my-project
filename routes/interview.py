from fastapi import APIRouter, UploadFile, File
from services.speech_service import speech_to_text

router = APIRouter()

@router.post("/interview/speech-to-text")
async def speech_to_text_api(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    text = speech_to_text(audio_bytes)
    print("Transcribed Text:", repr(text))
    return { "text": text }
