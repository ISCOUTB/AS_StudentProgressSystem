from fastapi import APIRouter, HTTPException, Depends
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth import login_user
from app.deps import get_session
from sqlmodel import Session

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, session: Session = Depends(get_session)):
    
    token = login_user(session, data.email, data.password)
    
    if not token:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    return {
        "access_token": token,
        "token_type": "bearer"
    }