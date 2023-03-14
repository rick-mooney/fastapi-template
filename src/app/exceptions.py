from fastapi import HTTPException, status


class Codes:
    UNAUTHORIZED = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not authorized for resource",
        headers={"WWW-Authenticate": "Bearer"},
    )
    DUPLICATE = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Item already exists",
        headers={"WWW-Authenticate": "Bearer"},
    )
    NOT_FOUND = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Item not found",
        headers={"WWW-Authenticate": "Bearer"},
    )
    NOT_IMPLEMENTED = HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="request type not implemented",
        headers={"WWW-Authenticate": "Bearer"},
    )
    INVALID_REQUEST = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid request",
        headers={"WWW-Authenticate": "Bearer"},
    )
