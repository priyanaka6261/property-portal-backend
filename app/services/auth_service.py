# Import User database model
from app.models.user_model import User

# Import security service for hashing & token generation
from app.core.security import security_service


class AuthService:
    """
    AuthService handles all authentication related business logic.

    Responsibilities:
    - Register new users
    - Validate login credentials
    - Generate JWT tokens
    """

    # =========================
    # REGISTER USER
    # =========================
    def register(self, db, user_data):
        """
        Registers new user in database.

        Parameters:
        db → Database session
        user_data → Data from request body
        """

        # Hash password before storing (security best practice)
        hashed_password = security_service.hash_password(user_data.password)

        # Create user object
        user = User(
            email=user_data.email,

            # Store hashed password
            password=hashed_password,

            # Store role (enum value converted to string)
            role=user_data.role.value
        )

        # Save user in database
        db.add(user)
        db.commit()

        return user

    # =========================
    # LOGIN USER
    # =========================

    def login(self, db, user_data):
        """
        Validates user login credentials and generates JWT token.
        """

        # Find user using email
        user = db.query(User).filter(User.email == user_data.email).first()

        # If user not found → login fails
        if not user:
            return None

        # Verify password using hashed password
        if not security_service.verify_password(user_data.password, user.password):
            return None

        # Create JWT token
        token = security_service.create_token({

            # VERY IMPORTANT → Include user ID for ownership logic
            "id": user.id,

            # Used for user identification
            "email": user.email,

            # Used for role-based authorization
            "role": user.role
        })

        # Return token to client
        return {"access_token": token}


# Create reusable service instance
auth_service = AuthService()
