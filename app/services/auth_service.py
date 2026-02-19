from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user_model import User
from app.core.security import hash_password, verify_password, create_access_token


class AuthService:

    # ✅ REGISTER
    def register_user(self, db: Session, email: str, password: str, role: str):

        existing_user = db.query(User).filter(User.email == email).first()

        if existing_user:
            raise HTTPException(
                status_code=400, detail="Email already registered")

        new_user = User(
            email=email,
            password=hash_password(password),
            role=role
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": "User registered successfully",
            "user_id": new_user.id
        }

    # ✅ LOGIN
    def login_user(self, db: Session, email: str, password: str):

        user = db.query(User).filter(User.email == email).first()

        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token({
            "id": user.id,
            "email": user.email,
            "role": user.role
        })

        return {"access_token": token, "token_type": "bearer"}


auth_service = AuthService()
