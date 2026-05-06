from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CourseCreate(BaseModel):
    title: str
    description: Optional[str] = None
    instructor_id: int
    is_published: Optional[int] = 0


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_published: Optional[int] = None


class CourseResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    instructor_id: int
    is_published: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
