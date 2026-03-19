import os
from pathlib import Path
from typing import List, Dict
import subprocess

VIDEOS_DIR = "data/videos"
SUPPORTED_FORMATS = [".mp4", ".mov", ".mkv", ".avi"]


def list_videos() -> List[Dict]:
    """List all videos in data/videos/"""
    videos = []
    if not os.path.exists(VIDEOS_DIR):
        os.makedirs(VIDEOS_DIR, exist_ok=True)
        return []
    
    for file in Path(VIDEOS_DIR).iterdir():
        if file.suffix.lower() in SUPPORTED_FORMATS:
            videos.append({
                "id": file.stem,
                "filename": file.name,
                "path": str(file.absolute()),
                "size_mb": round(file.stat().st_size / 1024 / 1024, 2)
            })
    
    return videos


def get_video_duration(video_path: str) -> int | None:
    """Get video duration in seconds using ffprobe"""
    try:
        result = subprocess.run([
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            video_path
        ], capture_output=True, text=True, check=True)
        return int(float(result.stdout.strip()))
    except:
        return None
