from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from app.db.db import get_session
from app.models.estudiante import Estudiantes
from app.core.security import verify_token

bearer = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    session: Session = Depends(get_session)
) -> Estudiantes:
    token = credentials.credentials
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token invalido o expirado")
    id_estudiante = payload.get("id")
    if not id_estudiante:
        raise HTTPException(status_code=401, detail="Token sin identificador")
    user = session.get(Estudiantes, id_estudiante)
    if not user:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return user