from pydantic import BaseModel


# Schema used when creating or updating property
class PropertyCreate(BaseModel):

    # Property title
    title: str

    # Property location
    location: str

    # Property price
    price: float

    # NEW → Status of property
    # Default automatically becomes "available"
    status: str = "available"


# Schema used for API response
class PropertyResponse(PropertyCreate):

    # Property ID returned in response
    id: int

    class Config:
        # Allows FastAPI to convert SQLAlchemy object to JSON
        from_attributes = True
