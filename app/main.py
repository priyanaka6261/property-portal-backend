from fastapi import FastAPI
from app.core.database import Base, engine
from app.api import auth_routes, property_routes


# Automatically creates tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Property Portal API")

# Register routes
app.include_router(auth_routes.router)
app.include_router(property_routes.router)
