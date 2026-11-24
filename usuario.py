from enum import Enum
from sqlalchemy import Column, Enum as SQLEnum, Integer, String

from database import Base


class PerfilUsuario(str, Enum):
    USUARIO = "usuario"
    ADMINISTRADOR = "administrador"


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False)
    email = Column(String(180), unique=True, index=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    perfil = Column(
        SQLEnum(PerfilUsuario, values_callable=lambda obj: [e.value for e in obj]),
        default=PerfilUsuario.USUARIO,
        nullable=False,
    )
