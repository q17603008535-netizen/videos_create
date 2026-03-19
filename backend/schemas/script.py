from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ScriptBase(BaseModel):
    content: str
    version: Optional[int] = 1
    # JSON string: array of title strings
    titles: Optional[str] = None
    # JSON string: array of tag strings
    tags: Optional[str] = None
    # JSON string: array of suggestion strings
    suggestions: Optional[str] = None
    status: Optional[str] = "draft"


class ScriptCreate(ScriptBase):
    video_id: int


class ScriptResponse(ScriptBase):
    id: int
    video_id: int
    created_at: datetime

    model_config = {"from_attributes": True}
