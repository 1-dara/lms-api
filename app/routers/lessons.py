from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.database import get_db
from app.models.lesson import Lesson
from app.models.course import Course
from app.models.user import User
from app.schemas.lesson import LessonCreate, LessonUpdate, LessonResponse
from app.routers.courses import get_current_user, get_instructor_or_admin

router = APIRouter()


@router.post("/", response_model=LessonResponse, status_code=201)
async def create_lesson(
    lesson: LessonCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_instructor_or_admin)
):
    # Verify course exists and user owns it (if not admin)
    result = await db.execute(select(Course).where(Course.id == lesson.course_id))
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if current_user.role != "admin" and course.instructor_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You can only add lessons to your own courses")

    new_lesson = Lesson(**lesson.model_dump())
    db.add(new_lesson)
    await db.commit()
    await db.refresh(new_lesson)
    return new_lesson


@router.get("/course/{course_id}", response_model=List[LessonResponse])
async def get_course_lessons(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Lesson).where(Lesson.course_id == course_id).order_by(Lesson.order))
    return result.scalars().all()


@router.put("/{lesson_id}", response_model=LessonResponse)
async def update_lesson(
    lesson_id: int,
    lesson_data: LessonUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_instructor_or_admin)
):
    result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
    lesson = result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    # Check course ownership
    course_result = await db.execute(select(Course).where(Course.id == lesson.course_id))
    course = course_result.scalar_one_or_none()
    if current_user.role != "admin" and course.instructor_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You can only edit lessons in your own courses")
    for field, value in lesson_data.model_dump(exclude_unset=True).items():
        setattr(lesson, field, value)
    await db.commit()
    await db.refresh(lesson)
    return lesson
