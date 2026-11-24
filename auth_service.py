from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from model.usuario import Usuario
from schema.usuario_schema import LoginRequest, TokenResponse
from security.security import criar_access_token, verificar_senha


def autenticar_usuario(db: Session, credenciais: LoginRequest) -> TokenResponse:
    email_normalizado = credenciais.email.strip().lower()
    usuario = db.query(Usuario).filter(Usuario.email == email_normalizado).first()

    if not usuario or not verificar_senha(credenciais.senha, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = criar_access_token(subject=usuario.id, perfil=usuario.perfil.value)
    return TokenResponse(access_token=token, token_type="bearer")
