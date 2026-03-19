import whisper
import os
from pathlib import Path
from typing import Dict, List
import subprocess

AUDIO_DIR = "data/audio"  # Extracted audio cache

def extract_audio(video_path: str) -> str:
    """Extract audio from video using ffmpeg"""
    os.makedirs(AUDIO_DIR, exist_ok=True)
    audio_path = os.path.join(AUDIO_DIR, Path(video_path).stem + ".wav")
    
    if not os.path.exists(audio_path):
        subprocess.run([
            "ffmpeg", "-y",
            "-i", video_path,
            "-vn", "-acodec", "pcm_s16le",
            "-ar", "16000", "-ac", "1",
            audio_path
        ], check=True, capture_output=True)
    
    return audio_path

def transcribe(video_path: str, language: str = "zh") -> Dict:
    """Transcribe video using Whisper medium model"""
    # Extract audio
    audio_path = extract_audio(video_path)
    
    # Load Whisper model (cached after first load)
    model = whisper.load_model("medium")
    
    # Transcribe
    result = model.transcribe(audio_path, language=language, verbose=False)
    
    return {
        "text": result["text"],
        "segments": result["segments"],
        "language": result["language"]
    }
