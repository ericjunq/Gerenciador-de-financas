from fastapi import APIRouter, Depends, HTTPException
from schemas import GanhosListResponse, GanhosSchema, GanhosResponse
from models import Ganhos, Usuario
from sqlalchemy.orm import Session
from dependencies import get_db
from security import get_current_user
from datetime import datetime, timedelta, timezone

ganhos_router = APIRouter(prefix='/ganhos', tags=['ganhos'])

@ganhos_router.post('/adicionar_ganho', response_model=GanhosResponse)
async def adicionar_ganho(ganhoschema: GanhosSchema, db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    novo_ganho = Ganhos(
        origem = ganhoschema.origem,
        descricao = ganhoschema.descricao,
        valor = ganhoschema.valor,
        usuario_id = usuario.id
    )

    db.add(novo_ganho)
    db.commit()
    db.refresh(novo_ganho)

    return novo_ganho


@ganhos_router.delete('/deletar_ganho/{ganho_id}')
async def deletar_ganho(ganho_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    ganho = db.query(Ganhos).filter(Ganhos.id == ganho_id, Ganhos.usuario_id == usuario.id).first()
    if ganho is None:
        raise HTTPException(status_code=404, detail='Ganho não encontrado')
    
    db.delete(ganho)
    db.commit()

    return {'message': 'Ganho deletado com sucesso'}

@ganhos_router.get('/listar_ganhos', response_model=GanhosListResponse)
async def listar_ganhos(filtro: str = 'mes', db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    hoje = datetime.now(timezone.utc)

    if filtro == 'dia':
        data_inicial = hoje.replace(hour=0, minute=0, second=0, microsecond=0)
    elif filtro == 'semana':
        data_inicial = hoje - timedelta(days=7)
    else:
        data_inicial = hoje.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    ganhos = db.query(Ganhos).filter(Ganhos.usuario_id == usuario.id, Ganhos.data >= data_inicial).all()

    total = sum(g.valor for g in ganhos)

    return {'ganhos': ganhos, 'total': total}