from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class VideoBase(BaseModel):
    original_filename: str
    # Duration in seconds
    duration: Optional[int] = None


class VideoCreate(VideoBase):
    file_path: str


class VideoResponse(VideoBase):
    id: int
    user_id: int
    file_path: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class VideoListResponse(BaseModel):
    videos: List[VideoResponse]
    total: int
