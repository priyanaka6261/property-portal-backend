from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user_schema import UserCreate, UserResponse, UserLogin
from app.services.auth_service import auth_service
from app.core.database import SessionLocal

router = APIRouter(prefix="/auth")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db=Depends(get_db)):
    return auth_service.register(db, user)


@router.post("/login")
def login(user: UserLogin, db=Depends(get_db)):

    token = auth_service.login(db, user)

    if not token:
        raise HTTPException(status_code=400, detail="Invalid Credentials")

    return token
