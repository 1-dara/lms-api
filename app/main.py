from fastapi import FastAPI
from app.routers import auth, courses, lessons

app = FastAPI(
    title="LMS API",
    description="Learning Management System Backend",
    version="1.0.0"
)

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(courses.router, prefix="/api/courses", tags=["Courses"])
app.include_router(lessons.router, prefix="/api/lessons", tags=["Lessons"])


@app.get("/")
async def root():
    return {"message": "LMS API is running 🎓"}
