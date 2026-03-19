import os
import pytest


def test_list_videos_empty():
    """Test listing videos when directory is empty or doesn't exist"""
    from backend.services.video_reader import list_videos
    
    videos = list_videos()
    assert isinstance(videos, list)


def test_list_videos_with_file():
    """Test listing videos when directory contains video files"""
    import os
    os.makedirs("data/videos", exist_ok=True)
    
    test_file = "data/videos/test.mp4"
    with open(test_file, "wb") as f:
        f.write(b"fake video")
    
    try:
        from backend.services.video_reader import list_videos
        videos = list_videos()
        assert len(videos) > 0
        assert videos[0]["filename"] == "test.mp4"
        assert videos[0]["id"] == "test"
        assert "path" in videos[0]
        assert "size_mb" in videos[0]
    finally:
        os.remove(test_file)


def test_list_videos_filters_supported_formats():
    """Test that only supported video formats are listed"""
    os.makedirs("data/videos", exist_ok=True)
    
    supported_files = ["video1.mp4", "video2.mov", "video3.mkv", "video4.avi"]
    unsupported_files = ["video5.txt", "video6.jpg", "video7.mp3"]
    
    created_files = []
    try:
        for filename in supported_files + unsupported_files:
            filepath = f"data/videos/{filename}"
            with open(filepath, "wb") as f:
                f.write(b"fake content")
            created_files.append(filepath)
        
        from backend.services.video_reader import list_videos
        videos = list_videos()
        
        video_filenames = [v["filename"] for v in videos]
        for supported in supported_files:
            assert supported in video_filenames
        
        for unsupported in unsupported_files:
            assert unsupported not in video_filenames
    finally:
        for filepath in created_files:
            if os.path.exists(filepath):
                os.remove(filepath)


def test_get_video_duration_none_on_invalid():
    """Test get_video_duration returns None for invalid paths"""
    from backend.services.video_reader import get_video_duration
    
    duration = get_video_duration("/nonexistent/path/video.mp4")
    assert duration is None
