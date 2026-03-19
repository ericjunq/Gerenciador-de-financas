from pwdlib import PasswordHash
from jose import JWTError, jwt
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from dependencies import get_db
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from models import Usuario


load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRES_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRES_MINUTES'))
REFRESH_TOKEN_EXPIRES_DAYS = int(os.getenv('REFRESH_TOKEN_EXPIRES_DAYS'))

oauth_scheme = OAuth2PasswordBearer(tokenUrl='users/login')


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

def verificar_refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(
            refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get('sub')
        return email
    
    except JWTError:
        return None

def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        email = payload.get('sub')

        if email is None:
            raise HTTPException(status_code=401, detail='Token inválido')
        
    except JWTError:
        raise HTTPException(status_code=401, detail='Token inválido')
    
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario is None:
        raise HTTPException(status_code=401, detail='Usuario não encontrado')
    
    return usuario