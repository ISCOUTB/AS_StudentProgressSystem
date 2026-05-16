# Importa BaseModel para crear esquemas con Pydantic
from pydantic import BaseModel, EmailStr


# Esquema de entrada para el login del usuario
class LoginRequest(BaseModel):
    
    # Email del usuario con validación de formato
    email: EmailStr

    # Contraseña del usuario
    password: str


# Esquema de respuesta para el token de autenticación
class TokenResponse(BaseModel):

    # Token de acceso (JWT normalmente)
    access_token: str

    # Tipo de token (ej: bearer)
    token_type: str