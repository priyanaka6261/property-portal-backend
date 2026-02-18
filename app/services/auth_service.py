from sqlalchemy.orm import Session
from app.models.user_model import User
from app.core.security import get_password_hash, verify_password, create_access_token


class AuthService:

    # REGISTER USER
    def register_user(self, db: Session, email: str, password: str, role: str):

        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            raise Exception("User already exists")

        hashed_password = get_password_hash(password)

        new_user = User(
            email=email,
            password=hashed_password,
            role=role
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": "User registered successfully",
            "user_id": new_user.id
        }

    # LOGIN USER

    def login_user(self, db: Session, email: str, password: str):

        user = db.query(User).filter(User.email == email).first()

        if not user:
            raise Exception("Invalid email")

        if not verify_password(password, user.password):
            raise Exception("Invalid password")

        token = create_access_token(
            {"user_id": user.id, "role": user.role}
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }
