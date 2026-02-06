from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.core.config import settings


# Argon2 hashing algorithm
pwd_context = CryptContext(schemes=["argon2"])


class SecurityService:

    # Converts plain password into hashed password
    def hash_password(self, password):
        return pwd_context.hash(password)

    # Verifies login password
    def verify_password(self, password, hashed):
        return pwd_context.verify(password, hashed)

    # Generates JWT token
    def create_token(self, data):

        payload = data.copy()

        # Token expiration
        payload["exp"] = datetime.utcnow() + timedelta(hours=2)

        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )

    # Decodes JWT token
    def decode_token(self, token):
        try:
            return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        except JWTError:
            return None


security_service = SecurityService()
