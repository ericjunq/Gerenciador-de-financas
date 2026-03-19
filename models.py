from sqlalchemy import String, Integer, Float, Boolean, ForeignKey, Column, DateTime
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime, timezone


class Base(DeclarativeBase):
    pass 

class Usuario(Base):

    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    sobrenome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    senha_hash = Column(String, nullable=False)
    cpf = Column(String, nullable=False)
    criado_em = Column(DateTime, default= lambda: datetime.now(timezone.utc))
    status = Column(Boolean, nullable=False, default=True)
    



