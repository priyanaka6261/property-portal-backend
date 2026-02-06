from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings


# Creates database connection
engine = create_engine(settings.DATABASE_URL)

# Creates session for executing queries
SessionLocal = sessionmaker(bind=engine)

# Base class for ORM models
Base = declarative_base()
