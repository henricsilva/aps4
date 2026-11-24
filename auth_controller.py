from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from schema.usuario_schema import LoginRequest, TokenResponse, UsuarioResponse
from security.dependencies import get_current_user
from service.auth_service import autenticar_usuario

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Autenticar usuário e obter token JWT",
)
def login(credenciais: LoginRequest, db: Session = Depends(get_db)):
    return autenticar_usuario(db=db, credenciais=credenciais)


@router.get(
    "/me",
    response_model=UsuarioResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar dados do usuário autenticado",
)
def obter_usuario_atual(current_user=Depends(get_current_user)):
    return current_user
