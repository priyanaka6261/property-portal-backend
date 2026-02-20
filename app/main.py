from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from app.api import auth_routes, property_routes
from app.core.database import Base, engine
from app.core.middleware import logging_middleware

# Create database tables
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Property Portal API",
    version="0.1.0",
    description="Secure Property Management API with JWT Authentication"
)
app.middleware("http")(logging_middleware)
# Include routers
app.include_router(auth_routes.router)
app.include_router(property_routes.router)
