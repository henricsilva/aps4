import re
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from model.usuario import PerfilUsuario


class UsuarioCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    senha: str = Field(..., min_length=8, max_length=128)

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, v: str) -> str:
        nome_limpo = v.strip()
        if not nome_limpo:
            raise ValueError("O nome não pode estar vazio.")
        return nome_limpo

    @field_validator("senha")
    @classmethod
    def validar_forca_senha(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("A senha não pode estar vazia.")
        if not re.search(r"[A-Za-z]", v) or not re.search(r"\d", v):
            raise ValueError("A senha deve conter pelo menos uma letra e um número.")
        return v


class UsuarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    email: EmailStr
    perfil: PerfilUsuario


class LoginRequest(BaseModel):
    email: EmailStr
    senha: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
