# Importa Annotated para tipado avanzado con dependencias
from typing import Annotated

# Importa herramientas principales de FastAPI
from fastapi import APIRouter, HTTPException, Depends

# Importa el formulario estándar OAuth2 para login
from fastapi.security import OAuth2PasswordRequestForm

# Importa la sesión de SQLModel para interactuar con la base de datos
from sqlmodel import Session

# Importa el esquema de respuesta del token
from app.schemas.auth import TokenResponse

# Importa el servicio encargado de autenticar usuarios
from app.services.auth import login_user

# Importa la función que proporciona la sesión de base de datos
from app.db.db import get_session


# Crea una instancia del router
router = APIRouter()


# Endpoint para iniciar sesión
@router.post(
    "/login",

    # Define el modelo de respuesta
    response_model=TokenResponse,

    # Define posibles respuestas HTTP
    responses={
        401: {"description": "Credenciales incorrectas"},
    }
)
def login(

    # Obtiene los datos enviados en el formulario OAuth2
    data: Annotated[OAuth2PasswordRequestForm, Depends()],

    # Inyecta automáticamente la sesión de base de datos
    session: Annotated[Session, Depends(get_session)]
):

    # Llama al servicio de autenticación
    # enviando username y password
    token = login_user(
        session,
        data.username,
        data.password
    )

    # Si no se genera token, las credenciales son inválidas
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas"
        )

    # Retorna el token JWT y el tipo de autenticación
    return {
        "access_token": token,
        "token_type": "bearer"
    }