from typing import TYPE_CHECKING, Optional
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from database import Base


class Script(Base):
    __tablename__ = "scripts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    video_id: Mapped[int] = mapped_column(ForeignKey("videos.id"), nullable=False)
    version: Mapped[int] = mapped_column(default=1)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    titles: Mapped[Optional[str]] = mapped_column(default=None)
    tags: Mapped[Optional[str]] = mapped_column(default=None)
    suggestions: Mapped[Optional[str]] = mapped_column(default=None)
    status: Mapped[str] = mapped_column(default="draft")
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    if TYPE_CHECKING:
        video: "Video"
    else:
        video = relationship("Video", back_populates="scripts")
