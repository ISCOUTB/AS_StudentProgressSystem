from models.user import fake_users_db
from utils.security import create_token

def login_user(email: str, password: str):
    
    # buscar usuario
    for user in fake_users_db:
        if user["email"] == email and user["password"] == password:
            
            token = create_token({
                "sub": user["email"],
                "id": user["id"]
            })

            return token

    return None
