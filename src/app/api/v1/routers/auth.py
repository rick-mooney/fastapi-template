from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from app.config import AUTH_COOKIE_ID, ACCESS_TOKEN_EXPIRE_MINUTES
from app.api.auth import authenticate_user, create_access_token, get_password_hash
from app.api.schemas import Token, UserOut, PasswordIn
from app.db.session import SessionManager
from app.db.crud import save_resource
from app.db.models import User
from datetime import timedelta
router = APIRouter(prefix="/api/v1")


@router.post("/token", response_model=Token)
async def login_for_access_token(
    response: Response, form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "scopes": user.scopes},
        expires_delta=access_token_expires,
    )
    response.set_cookie(
        key=AUTH_COOKIE_ID,
        value=f"Bearer {access_token}",
        httponly=True,
        samesite="none",
        secure=True,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token/{token}")
async def validate_access_token(token: str, p: PasswordIn):
    with SessionManager() as db:
        user = db.query(User).filter(User.reset_token == token).first()
        if user:
            user.reset_token = None
            user.password = get_password_hash(p.password)
            new_user = save_resource(db, user, user.id)
            new_user.scopes = new_user.scopes.split(" ")
            return UserOut.from_orm(user)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token not valid or expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
