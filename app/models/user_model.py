from sqlalchemy import Column, Integer, String
from app.core.database import Base
from app.models.role_enum import UserRole


# User database table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)

    # Role stored using enum value
    role = Column(String, default=UserRole.user.value)
