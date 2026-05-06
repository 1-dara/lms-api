from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class LessonCreate(BaseModel):
    title: str
    content: Optional[str] = None
    video_url: Optional[str] = None
    course_id: int
    order: Optional[int] = 0


class LessonUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    video_url: Optional[str] = None
    order: Optional[int] = None


class LessonResponse(BaseModel):
    id: int
    title: str
    content: Optional[str]
    video_url: Optional[str]
    course_id: int
    order: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
