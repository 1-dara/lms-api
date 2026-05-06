from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.models.user import UserRole


class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.STUDENT


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
