from fastapi import APIRouter, Depends, HTTPException
from schemas import UsuarioResponse, UsuarioSchema, LoginSchema, TokenResponse
from sqlalchemy.orm import Session
from dependencies import get_db
from models import Usuario
from validations import validate_cpf
from security import criptografar_senha, verificar_senha, criar_refresh_token, criar_access_token


auth_router = APIRouter()

@auth_router.post('/criar_conta', response_model=UsuarioResponse)
async def criar_usuario(usuario: UsuarioSchema, db: Session = Depends(get_db)):
    cpf_valido = validate_cpf(usuario.cpf)
    if not cpf_valido:
        raise HTTPException(status_code=400, detail='CPF inválido')

    email = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if email:
        raise HTTPException(status_code=409, detail='Email já cadastrado')
    
    cpf_existente = db.query(Usuario).filter(Usuario.cpf == usuario.cpf).first()
    if cpf_existente:
        raise HTTPException(status_code=409, detail='CPF já cadastrado')
    
    senha_hash = criptografar_senha(usuario.senha)

    novo_usuario = Usuario(
        nome = usuario.nome,
        sobrenome = usuario.sobrenome,
        email = usuario.email, 
        senha_hash = senha_hash,
        cpf = usuario.cpf
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    
    return novo_usuario

@auth_router.post('/login', response_model=TokenResponse)
async def login(login_schema: LoginSchema, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == login_schema.email).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')
    
    if not verificar_senha(login_schema.senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail='Senha incorreta')
    
    access_token = criar_access_token(
    dados={'sub': usuario.email, 'type': 'access'}
)

    refresh_token = criar_refresh_token(
    dados={'sub': usuario.email, 'type': 'refresh'}
)

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer'
    }
