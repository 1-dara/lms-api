from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.database import get_db
from app.models.course import Course
from app.models.user import User
from app.schemas.course import CourseCreate, CourseUpdate, CourseResponse
from app.core.security import verify_access_token
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = int(payload.get("sub"))
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


async def get_instructor_or_admin(current_user: User = Depends(get_current_user)):
    if current_user.role not in ["admin", "instructor"]:
        raise HTTPException(
            status_code=403, detail="Only instructors/admins can create/edit courses")
    return current_user


@router.post("/", response_model=CourseResponse, status_code=201)
async def create_course(
    course: CourseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_instructor_or_admin)
):
    new_course = Course(**course.model_dump())
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    return new_course


@router.get("/", response_model=List[CourseResponse])
async def get_courses(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course))
    return result.scalars().all()


@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: int,
    course_data: CourseUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_instructor_or_admin)
):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if current_user.role != "admin" and course.instructor_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You can only update your own courses")
    for field, value in course_data.model_dump(exclude_unset=True).items():
        setattr(course, field, value)
    await db.commit()
    await db.refresh(course)
    return course
