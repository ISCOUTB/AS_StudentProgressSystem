from fastapi import APIRouter, HTTPException
from schemas.auth_schema import LoginRequest, TokenResponse
from services.auth_service import login_user

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
