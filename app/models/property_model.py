from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.core.database import Base


class Property(Base):
    __tablename__ = "properties"

    # Primary key of property
    id = Column(Integer, primary_key=True)

    # Property title
    title = Column(String)

    # Property location
    location = Column(String)

    # Property price
    price = Column(Float)

    # Stores user who created property
    # Links property with users table
    owner_id = Column(Integer, ForeignKey("users.id"))

    # NEW FEATURE → Property availability status
    # Default value = available
    status = Column(String, default="available")


# explaination
'''Links property to user
Stores who created property
Enables ownership checking'''
