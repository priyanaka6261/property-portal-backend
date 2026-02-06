# BaseSettings is used to manage environment variables easily

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./property.db"
    SECRET_KEY: str = "secret"
    ALGORITHM: str = "HS256"


settings = Settings()

# DATABASE_URL defines database connection string
# SQLite is used here for simplicity and local development

# SECRET_KEY is used to sign and encrypt JWT tokens

# ALGORITHM defines encryption algorithm for JWT tokens


# Creating a global settings object for reuse across project
