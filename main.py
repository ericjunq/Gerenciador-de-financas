from fastapi import FastAPI
from auth_routers import auth_router
from models import Base
from database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)



