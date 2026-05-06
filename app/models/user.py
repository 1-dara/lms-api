from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base
import enum


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    INSTRUCTOR = "instructor"
    STUDENT = "student"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.STUDENT)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc))

    courses_teaching = relationship("Course", back_populates="instructor")
    enrollments = relationship("Enrollment", back_populates="student")
