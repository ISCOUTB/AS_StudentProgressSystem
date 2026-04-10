from models.estudiante import Estudiantes
from core.security import create_token


def login_user(email: str, password: str):

# buscar usuario
    for user in fake_users_db:
    # REVISAR
        if Estudiantes.correo == email and Estudiantes.hash_password == password:

            token = create_token({
                "sub": user["email"],
                "id": user["id"]
            })

            return token

    return None