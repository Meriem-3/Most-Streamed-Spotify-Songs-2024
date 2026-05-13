import bcrypt
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

# recupère la Clé secrète(.env) pour signer les tokens JWT
SECRET_KEY = os.getenv("SECRET_KEY")

# Hachage du mdp

def hash_password(password: str) -> str:

    #Transforme un mdp en hash
    password_bytes = password.encode("utf-8") #transforme le mot de passe en bytes
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt(rounds=12))
    return hashed.decode("utf-8")#convertit le hash en string


# Compare le mot de passe entré par l’utilisateur avec le hash stocké

def verify_password(password: str, hashed_password: str) -> bool:
    
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


# Création d'un token JWT

def create_token(user_id: int, expires_minutes=30) -> str:

    #Crée un token JWT contenant l'id utilisateur
    
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=expires_minutes)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token



# Vérification du token JWT

def verify_token(token: str):
    
    #retourne le payload si valide, sinon none

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        print("Token expiré.")
        return None
    except jwt.InvalidTokenError:
        print("Token invalide.")
        return None