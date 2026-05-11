from sqlmodel import Session, select
from app.models.estudiante import Estudiantes
from app.core.security import create_token
import hashlib


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def login_user(db: Session, email: str, password: str):

    statement = select(Estudiantes).where(
        Estudiantes.correo == email
    )

    user = db.exec(statement).first()

    print("EMAIL:", email)
    print("PASSWORD:", password)
    print("HASH INPUT:", hash_password(password))
    print("USER:", user)

    if user:
        print("DB HASH:", user.hash_password)
        print("DB EMAIL:", user.correo)

    if user and user.hash_password == hash_password(password):

        token = create_token({
            "sub": user.correo,
            "id": str(user.id_estudiante)
        })

        return token

    return None