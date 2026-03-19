from pydantic import BaseModel, EmailStr
from typing import Optional

class UsuarioResponse(BaseModel):
    nome: str
    sobrenome: str
    email: EmailStr
    
    class Config: 
        from_attributes = True

class UsuarioSchema(BaseModel):
    nome: str 
    sobrenome: str 
    email: EmailStr 
    senha: str 
    cpf: str 

class LoginSchema(BaseModel):
    email : EmailStr 
    senha : str 

class TokenResponse(BaseModel):
    access_token : str 
    refresh_token: str
    token_type: str 

