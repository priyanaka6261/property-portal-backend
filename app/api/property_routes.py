from fastapi import APIRouter, Depends
from app.schemas.property_schema import PropertyCreate, PropertyResponse
from app.services.property_service import property_service
from app.dependencies.auth_dependency import get_current_user
from app.core.database import SessionLocal

router = APIRouter(prefix="/properties")


# Database dependency
# Creates DB session and closes automatically
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------------------------------------
# CREATE PROPERTY
# ------------------------------------------------
@router.post("/", response_model=PropertyResponse)
def create_property(
    property: PropertyCreate,
    db=Depends(get_db),

    # Extract logged-in user from JWT token
    user=Depends(get_current_user)
):

    return property_service.create_property(db, property, user)


# ------------------------------------------------
# SEARCH & FILTER PROPERTIES
# ------------------------------------------------
@router.get("/search")
def search_property(
    location: str = None,       # Optional location filter
    min_price: float = None,    # Optional min price filter
    max_price: float = None,    # Optional max price filter
    db=Depends(get_db)
):

    return property_service.search_properties(
        db, location, min_price, max_price
    )


# ------------------------------------------------
# GET LOGGED USER PROPERTIES
# ------------------------------------------------
@router.get("/my-properties")
def my_properties(
    db=Depends(get_db),

    # Gets user data from JWT token
    user=Depends(get_current_user)
):

    return property_service.get_my_properties(db, user)


# ------------------------------------------------
# DASHBOARD STATISTICS
# ------------------------------------------------
@router.get("/stats")
def stats(db=Depends(get_db)):

    return property_service.property_stats(db)
