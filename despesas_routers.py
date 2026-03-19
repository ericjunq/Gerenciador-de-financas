from fastapi import APIRouter, Depends, HTTPException
from schemas import DespesasListResponse, DespesasResponse, DespesasSchema
from models import Despesas, Usuario
from sqlalchemy.orm import Session
from dependencies import get_db
from security import get_current_user
from datetime import datetime, timedelta, timezone

despesas_router = APIRouter(prefix='/despesas', tags=['despesas'])

@despesas_router.post('/adicionar_despesa', response_model=DespesasResponse)
async def adicionar_despesa(despesaschema: DespesasSchema, db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    nova_despesa = Despesas(
        categoria = despesaschema.categoria,
        descricao = despesaschema.descricao,
        valor = despesaschema.valor,
        usuario_id = usuario.id
    )

    db.add(nova_despesa)
    db.commit()
    db.refresh(nova_despesa)

    return nova_despesa

@despesas_router.delete('/deletar_despesa/{despesa_id}')
async def deletar_despesa(despesa_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    despesa = db.query(Despesas).filter(Despesas.id == despesa_id, Despesas.usuario_id == usuario.id).first()
    if despesa is None:
        raise HTTPException(status_code=404, detail='Despesa não encontrada')
    
    db.delete(despesa)
    db.commit()

    return {'message': 'Despesa deletada com sucesso'}

@despesas_router.get('/listar_despesas', response_model=DespesasListResponse)
async def listar_despesas(filtro: str = 'mes', db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    hoje = datetime.now(timezone.utc)

    if filtro == 'dia':
        data_inicio = hoje.replace(hour=0, minute=0, second=0, microsecond=0)
    elif filtro == 'semana':
        data_inicio = hoje - timedelta(days=7)
    else:
        data_inicio = hoje.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    despesas = db.query(Despesas).filter(Despesas.usuario_id == usuario.id, Despesas.data >= data_inicio).all()

    total = sum(d.valor for d in despesas)

    return {'despesas': despesas, 'total': total}

