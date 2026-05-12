from fastapi import FastAPI
from app.routers import auth, courses, lessons, images

app = FastAPI(
    title="LMS API",
    description="Learning Management System",
    version="1.0.0"
)

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(courses.router, prefix="/api/courses", tags=["Courses"])
app.include_router(lessons.router, prefix="/api/lessons", tags=["Lessons"])
app.include_router(images.router, prefix="/api", tags=["Images"])

@app.get("/")
async def root():
    return {"message": "LMS API is running 📚"}