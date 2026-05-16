```python id="r1m8qp"
# Importa Depends y HTTPException para manejar dependencias y errores HTTP
from fastapi import Depends, HTTPException

# Importa esquema de autenticación Bearer para leer el token del header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Importa Session para acceso a base de datos
from sqlmodel import Session

# Importa dependencia de sesión de base de datos
from app.db.db import get_session

# Importa modelo de estudiantes
from app.models.estudiante import Estudiantes

# Importa función para verificar el token JWT
from app.core.security import verify_token

# Importa Annotated para tipado de dependencias
from typing import Annotated


# Esquema de autenticación Bearer (Authorization: Bearer <token>)
bearer = HTTPBearer()


# Obtiene el usuario actual a partir del token JWT
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    session: Session = Depends(get_session)
) -> Estudiantes:

    # Extrae el token del header Authorization
    token = credentials.credentials

    # Verifica y decodifica el token
    payload = verify_token(token)

    # Si el token no es válido o expiró, lanza error 401
    if not payload:
        raise HTTPException(status_code=401, detail="Token invalido o expirado")

    # Obtiene el ID del estudiante desde el token
    id_estudiante = payload.get("id")

    # Si no existe el ID en el token, lanza error 401
    if not id_estudiante:
        raise HTTPException(status_code=401, detail="Token sin identificador")

    # Busca el usuario en la base de datos
    user = session.get(Estudiantes, id_estudiante)

    # Si no existe el usuario, lanza error 404
    if not user:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    return user


# Alias tipado para usarlo fácilmente como dependencia en rutas protegidas
CurrentUser = Annotated[Estudiantes, Depends(get_current_user)]
```
