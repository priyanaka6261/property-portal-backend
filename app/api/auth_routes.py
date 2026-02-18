from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.auth_dependency import get_db
from app.core.database import get_db

from app.schemas.user_schema import RegisterRequest, LoginRequest
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])
auth_service = AuthService()


@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    return auth_service.register_user(
        db,
        data.email,
        data.password,
        data.role
    )


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.login_user(
        db,
        data.email,
        data.password
    )
