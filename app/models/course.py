from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    instructor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_published = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(
        timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    instructor = relationship("User", back_populates="courses_teaching")
    lessons = relationship(
        "Lesson", back_populates="course", cascade="all, delete-orphan")
