from sqlmodel import Session, select
from app.models.estudiante import Estudiantes
from app.core.security import create_token

def login_user(db: Session, email: str, password: str):

    # consulta usando SQLModel
    statement = select(Estudiantes).where(Estudiantes.correo == email)
    user = db.exec(statement).first()

    if user and user.hash_password == password:

        token = create_token({
            "sub": user.correo,
            "id": user.id
        })

        return token

    return None
