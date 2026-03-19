from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from database import Base


class Video(Base):
    __tablename__ = "videos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    file_path: Mapped[str] = mapped_column(nullable=False)
    original_filename: Mapped[str] = mapped_column(nullable=False)
    duration: Mapped[Optional[int]] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(default="pending")
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    if TYPE_CHECKING:
        user: "User"
        scripts: List["Script"] = []
    else:
        user = relationship("User", back_populates="videos")
        scripts = relationship("Script", back_populates="video", cascade="all, delete-orphan")
