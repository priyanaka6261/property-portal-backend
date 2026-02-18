from fastapi import APIRouter, Depends
from app.schemas.property_schema import PropertyCreate, PropertyResponse
from app.services.property_service import property_service
from app.dependencies.auth_dependency import get_current_user
from app.core.database import get_db

router = APIRouter(prefix="/properties")


@router.post("/", response_model=PropertyResponse)
def create_property(property: PropertyCreate, db=Depends(get_db), user=Depends(get_current_user)):
    return property_service.create_property(db, property, user)


@router.put("/{property_id}", response_model=PropertyResponse)
def update_property(property_id: int, property: PropertyCreate, db=Depends(get_db), user=Depends(get_current_user)):
    return property_service.update_property(db, property_id, property, user)


@router.delete("/{property_id}")
def delete_property(property_id: int, db=Depends(get_db), user=Depends(get_current_user)):
    return property_service.delete_property(db, property_id, user)


@router.get("/my-properties")
def my_properties(db=Depends(get_db), user=Depends(get_current_user)):
    return property_service.get_my_properties(db, user)


@router.get("/search")
def search(location: str = None, min_price: float = None, max_price: float = None, db=Depends(get_db)):
    return property_service.search_properties(db, location, min_price, max_price)


@router.get("/stats")
def stats(db=Depends(get_db)):
    return property_service.property_stats(db)
