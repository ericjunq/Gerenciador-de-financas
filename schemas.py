from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum
from datetime import datetime

# Usuarios
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

# Despesas
class CategoriasEnum(str, Enum):
    alimentacao = 'alimentacao'
    transporte = 'transporte'
    moradia = 'moradia'
    saude = 'saude'
    educacao = 'educacao'
    vestuario = 'vestuario'
    esporte = 'esporte'
    outros = 'outros'

class DespesasResponse(BaseModel):
    id: int 
    categoria: CategoriasEnum
    descricao: Optional[str] = None
    valor: float 
    data: datetime 

    class Config: 
        from_attributes = True

class DespesasListResponse(BaseModel):
    despesas: list[DespesasResponse]
    total: float 

class DespesasSchema(BaseModel):
    categoria: CategoriasEnum 
    descricao: Optional[str] = None 
    valor : float

# Ganhos
class OrigensEnum(str, Enum):
    salario = 'salario'
    freelance = 'freelance'
    investimento = 'investimento'
    bonus = 'bonus'
    outros = 'outros'

class GanhosResponse(BaseModel):
    id: int 
    origem: OrigensEnum
    descricao: Optional[str] = None
    valor: float 
    data: datetime

    class Config:
        from_attributes = True

class GanhosListResponse(BaseModel):
    ganhos: list[GanhosResponse]
    total: float

class GanhosSchema(BaseModel):
    origem: OrigensEnum
    descricao: Optional[str] = None 
    valor: float 

# Relatório

class RelatorioResponse(BaseModel):
    relatorio: str 