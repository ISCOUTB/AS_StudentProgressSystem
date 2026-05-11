from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from app.schemas.auth import TokenResponse
from app.services.auth import login_user
from app.db.db import get_session


router = APIRouter()


@router.post(
    "/login",
    response_model=TokenResponse,
    responses={
        401: {"description": "Credenciales incorrectas"},
    }
)
def login(
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[Session, Depends(get_session)]
):

    token = login_user(
        session,
        data.username,
        data.password
    )

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas"
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }