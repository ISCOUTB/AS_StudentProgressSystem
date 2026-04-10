from fastapi import APIRouter, HTTPException
from schemas.auth import LoginRequest, TokenResponse
from services.auth import login_user

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):

    token = login_user(data.email, data.password)

    if not token:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    return {
        "access_token": token,
        "token_type": "bearer"
    }