"""
Property business logic.
Handles role-based access and ownership.
"""

from app.models.property_model import Property
from app.models.property_model import Property
from sqlalchemy import func
from fastapi import HTTPException
from sqlalchemy.orm import Session


class PropertyService:

    def create_property(self, db: Session, property_data, user):

        # ✅ user is dict → use []
        if user["role"] not in ["admin", "agent"]:
            raise HTTPException(
                status_code=403, detail="Not allowed to create property")

        new_property = Property(
            title=property_data.title,
            location=property_data.location,
            price=property_data.price,
            status=property_data.status,
            owner_id=user["id"]
        )

        db.add(new_property)
        db.commit()
        db.refresh(new_property)

        return new_property
        """
        Only admin or agent can create property.
        """

        # FIX: user is dict → use ["role"]

    def get_my_properties(self, db, user):
        """
        Get properties owned by user.
        """
        return db.query(Property).filter(Property.owner_id == user["id"]).all()

    def delete_property(self, db, property_id, user):
        """
        Admin OR owner can delete.
        """

        prop = db.query(Property).filter(Property.id == property_id).first()

        if not prop:
            return None

        # FIX: dict access
        if user["role"] != "admin" and prop.owner_id != user["id"]:
            raise Exception("Not authorized")

        db.delete(prop)
        db.commit()

        return prop

    def property_stats(self, db):
        """
       Returns property statistics count by status.
       Used for dashboard / analytics.
       """
        stats = db.query(
            Property.status,
            func.count(Property.id)
        ).group_by(Property.status).all()

        # Convert to dictionary
        result = {status: count for status, count in stats}

        return result

    def update_property(self, db, property_id, property_data, user):
        prop = db.query(Property).filter(Property.id == property_id).first()

        if not prop:
            raise Exception("Property not found")

        # Only admin OR owner allowed
        if user["role"] != "admin" and prop.owner_id != user["id"]:
            raise Exception("Not authorized to update property")

        # Update fields
        prop.title = property_data.title
        prop.location = property_data.location
        prop.price = property_data.price
        prop.status = property_data.status

        db.commit()
        db.refresh(prop)

        return prop
        # ✅ SEARCH PROPERTIES

    def search_properties(self, db, location=None, min_price=None, max_price=None):

        query = db.query(Property)

        if location:
            query = query.filter(Property.location.ilike(f"%{location}%"))

        if min_price:
            query = query.filter(Property.price >= min_price)

        if max_price:
            query = query.filter(Property.price <= max_price)

        return query.all()

    def get_all_properties(self, db):
        properties = db.query(Property).all()

        return [
            {
                "id": p.id,
                "title": p.title,
                "price": p.price,
                "location": p.location,
                "status": p.status,
                "owner_id": p.owner_id
            }
            for p in properties
        ]


property_service = PropertyService()
