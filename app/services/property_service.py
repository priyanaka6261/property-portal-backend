from app.models.property_model import Property


class PropertyService:

    # ------------------------------------------------
    # CREATE PROPERTY
    # ------------------------------------------------
    def create_property(self, db, property_data, user):

        # Create property object
        prop = Property(
            title=property_data.title,
            location=property_data.location,
            price=property_data.price,
            status=property_data.status,

            # Assign ownership using logged-in user
            owner_id=user["id"]
        )

        db.add(prop)
        db.commit()

        return prop

    # ------------------------------------------------
    # SEARCH + FILTER PROPERTIES
    # ------------------------------------------------

    def search_properties(self, db, location=None, min_price=None, max_price=None):

        # Start base query
        query = db.query(Property)

        # Filter by location (partial matching allowed)
        if location:
            query = query.filter(Property.location.contains(location))

        # Filter by minimum price
        if min_price:
            query = query.filter(Property.price >= min_price)

        # Filter by maximum price
        if max_price:
            query = query.filter(Property.price <= max_price)

        return query.all()

    # ------------------------------------------------
    # GET ONLY LOGGED USER PROPERTIES
    # ------------------------------------------------

    def get_my_properties(self, db, user):

        # Returns properties created by current user
        return db.query(Property).filter(
            Property.owner_id == user["id"]
        ).all()

    # ------------------------------------------------
    # DASHBOARD STATISTICS
    # ------------------------------------------------

    def property_stats(self, db):

        # Count total properties
        total = db.query(Property).count()

        # Count available properties
        available = db.query(Property).filter(
            Property.status == "available"
        ).count()

        # Count sold properties
        sold = db.query(Property).filter(
            Property.status == "sold"
        ).count()

        return {
            "total_properties": total,
            "available_properties": available,
            "sold_properties": sold
        }


property_service = PropertyService()
