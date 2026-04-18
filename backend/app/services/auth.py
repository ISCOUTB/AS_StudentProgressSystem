from sqlalchemy.orm import Session
from models.estudiante import Estudiantes
from core.security import create_token

def login_user(db: Session, email: str, password: str):

    # buscar usuario en la BD
    user = db.query(Estudiantes).filter(Estudiantes.correo == email).first()

    if user and user.hash_password == password:

        token = create_token({
            "sub": user.correo,
            "id": user.id
        })

        return token

    return None
