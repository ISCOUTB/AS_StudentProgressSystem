# Importa Session y select para consultas a la base de datos con SQLModel
from sqlmodel import Session, select

# Importa el modelo de estudiantes
from app.models.estudiante import Estudiantes

# Importa la función para crear el token JWT
from app.core.security import create_token

# Importa hashlib para generar hashes de contraseña
import hashlib


# Función para encriptar la contraseña usando SHA256
def hash_password(password: str) -> str:
    
    # Convierte la contraseña a bytes y genera el hash
    return hashlib.sha256(password.encode()).hexdigest()


# Función encargada de autenticar al usuario
def login_user(db: Session, email: str, password: str):

    # Construye la consulta para buscar el usuario por correo
    statement = select(Estudiantes).where(
        Estudiantes.correo == email
    )

    # Ejecuta la consulta y obtiene el primer resultado
    user = db.exec(statement).first()

    # Debug: imprime datos recibidos
    print("EMAIL:", email)
    print("PASSWORD:", password)
    print("HASH INPUT:", hash_password(password))
    print("USER:", user)

    # Si el usuario existe, imprime información de la base de datos
    if user:
        print("DB HASH:", user.hash_password)
        print("DB EMAIL:", user.correo)

    # Valida que el usuario exista y que la contraseña coincida
    if user and user.hash_password == hash_password(password):

        # Genera el token JWT con información del usuario
        token = create_token({
            "sub": user.correo,
            "id": str(user.id_estudiante)
        })

        # Retorna el token generado
        return token

    # Si falla la autenticación, retorna None
    return None