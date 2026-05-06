from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    video_url = Column(String, nullable=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(
        timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    course = relationship("Course", back_populates="lessons")
