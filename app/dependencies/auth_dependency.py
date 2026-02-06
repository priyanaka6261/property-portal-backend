from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from app.core.security import security_service
from app.models.role_enum import UserRole


# Extracts token from request
security = HTTPBearer()


def get_current_user(credentials=Depends(security)):

    token = credentials.credentials
    payload = security_service.decode_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid Token")

    return payload


# Role based authorization
def require_role(role: UserRole):

    def role_checker(user=Depends(get_current_user)):

        if user["role"] != role.value:
            raise HTTPException(status_code=403, detail="Access Denied")

        return user

    return role_checker
