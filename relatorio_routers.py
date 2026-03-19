from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from security import get_current_user
from dependencies import get_db
from ia_service import gerar_relatorio
from datetime import datetime, timedelta, date, timezone
from schemas import RelatorioResponse
from models import Usuario, Ganhos, Despesas
from calendar import monthrange

gerador_de_relatorio = APIRouter(prefix='/relatorio', tags=['relatorio'])

@gerador_de_relatorio.post('/gerar_relatorio', response_model=RelatorioResponse)
async def gerador_relatorio(mes: int = date.today().month, ano: int = date.today().year, db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    data_inicio = datetime(ano, mes, 1, tzinfo=timezone.utc)
    ultimo_dia = monthrange(ano, mes)[1]
    data_final = datetime(ano, mes, ultimo_dia, 23, 59, 59, tzinfo=timezone.utc)

    despesas = db.query(Despesas).filter(
        Despesas.usuario_id == usuario.id,
        Despesas.data >= data_inicio,
        Despesas.data <= data_final
        ).all()
    
    ganhos = db.query(Ganhos).filter(
        Ganhos.usuario_id == usuario.id,
        Ganhos.data >= data_inicio,
        Ganhos.data <= data_final
    ).all()

    total_despesas = sum(d.valor for d in despesas)
    total_ganhos = sum(g.valor for g in ganhos)
    saldo = total_ganhos - total_despesas

    breakdown_ganhos = {}
    for ganho in ganhos:
        origem = ganho.origem
        if origem not in breakdown_ganhos:
            breakdown_ganhos[origem] = 0
        breakdown_ganhos[origem] += ganho.valor
    
    breakdown_despesas = {}
    for despesa in despesas:
        categoria = despesa.categoria
        if not categoria in breakdown_despesas:
            breakdown_despesas[categoria] = 0
        breakdown_despesas[categoria] += despesa.valor

    relatorio = gerar_relatorio(
        total_ganhos,
        total_despesas,
        saldo,
        breakdown_ganhos,
        breakdown_despesas,
        mes,
        ano
    )

    return {'relatorio': relatorio}

