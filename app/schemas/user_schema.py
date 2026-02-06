from pydantic import BaseModel, EmailStr
from app.models.role_enum import UserRole


# Used when registering user
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole = UserRole.user


# Used during login
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Used in API response
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True
