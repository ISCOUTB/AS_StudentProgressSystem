from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from utils.security import verify_token

security = HTTPBearer()

def get_current_user(credentials = Depends(security)):
    token = credentials.credentials
    data = verify_token(token)

    if not data:
        raise HTTPException(status_code=401, detail="Token inválido")

    return data
