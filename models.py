from sqlalchemy import String, Integer, Float, Boolean, ForeignKey, Column, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime, timezone


class Base(DeclarativeBase):
    pass 

class Usuario(Base):

    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(20), nullable=False)
    sobrenome = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    senha_hash = Column(String(255), nullable=False)
    cpf = Column(String(11), nullable=False)
    criado_em = Column(DateTime, default= lambda: datetime.now(timezone.utc))
    status = Column(Boolean, nullable=False, default=True)
    
    despesas = relationship('Despesas', back_populates='usuario')
    ganhos = relationship('Ganhos', back_populates='usuario')

class Despesas(Base):
    
    __tablename__ = 'despesas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    categoria = Column(String(20), nullable=False)
    descricao = Column(String(40), nullable=True)
    valor = Column(Float, nullable=False)
    data = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    usuario = relationship('Usuario', back_populates='despesas')

class Ganhos(Base):

    __tablename__ = 'ganhos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    origem = Column(String(30), nullable=False)
    descricao = Column(String(50), nullable=True)
    valor = Column(Float, nullable=False)
    data = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    usuario = relationship('Usuario', back_populates='ganhos')
