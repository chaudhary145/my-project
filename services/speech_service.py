import os
import tempfile
import subprocess
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()

FFMPEG_PATH = r"C:\ffmpeg\ffmpeg-master-latest-win64-gpl-shared\ffmpeg-master-latest-win64-gpl-shared\bin\ffmpeg.exe"

def speech_to_text(audio_bytes: bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as f:
        f.write(audio_bytes)
        input_path = f.name

    output_path = input_path.replace(".ogg", ".wav")
    subprocess.run(
        [
            FFMPEG_PATH,
            "-y",
            "-i", input_path,
            "-ar", "16000",
            "-ac", "1",
            "-c:a", "pcm_s16le",
            output_path
        ],
        check=True
    )
    speech_config = speechsdk.SpeechConfig(
        subscription=os.getenv("AZURE_SPEECH_KEY"),
        region=os.getenv("AZURE_REGION")
    )
    audio_config = speechsdk.audio.AudioConfig(filename=output_path)
    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,
        audio_config=audio_config
    )
    result = recognizer.recognize_once()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    return ""
