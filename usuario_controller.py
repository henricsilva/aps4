from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from schema.usuario_schema import UsuarioCreate, UsuarioResponse
from service.usuario_service import criar_usuario

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


@router.post(
    "",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar novo usuário",
)
def cadastrar_usuario(dados: UsuarioCreate, db: Session = Depends(get_db)):
    return criar_usuario(db=db, dados=dados)
