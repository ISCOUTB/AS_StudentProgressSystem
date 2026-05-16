from datetime import datetime, timezone, timedelta
import jwt
import os

# Clave secreta para firmar tokens JWT (debe cambiarse en producción)
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"

def create_token(data: dict):
    """Genera un JWT con los datos dados y expiración de 60 minutos."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token: str):
    """Decodifica y valida un JWT. Retorna el payload o None si es inválido/expirado."""
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded
    except (jwt.InvalidTokenError, jwt.DecodeError, jwt.ExpiredSignatureError):
        return None
