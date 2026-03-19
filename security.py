from pwdlib import PasswordHash
from jose import JWTError, jwt
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRES_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRES_MINUTES'))
REFRESH_TOKEN_EXPIRES_DAYS = int(os.getenv('REFRESH_TOKEN_EXPIRES_DAYS'))


password_hash = PasswordHash.recommended()

def criptografar_senha(senha):
    return password_hash.hash(senha)

def verificar_senha(senha, senha_hash):
    return password_hash.verify(senha, senha_hash)

def criar_access_token(dados: dict):
    to_encode = dados.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({'exp': expire})

    access_token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return access_token

def criar_refresh_token(dados: dict):
    to_encode = dados.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRES_DAYS)
    to_encode.update({'exp': expire})

    refresh_token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return refresh_token


#def get_current_user()