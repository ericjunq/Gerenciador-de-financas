from fastapi import FastAPI
from auth_routers import auth_router
from models import Base
from database import engine
from despesas_routers import despesas_router
from ganhos_routers import ganhos_router
from relatorio_routers import gerador_de_relatorio

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(ganhos_router)
app.include_router(despesas_router)
app.include_router(gerador_de_relatorio)