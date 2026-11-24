import os
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from model.usuario import PerfilUsuario, Usuario
from schema.usuario_schema import UsuarioCreate
from security.security import gerar_hash_senha


def criar_usuario(db: Session, dados: UsuarioCreate) -> Usuario:
    email_normalizado = dados.email.strip().lower()

    existente = db.query(Usuario).filter(Usuario.email == email_normalizado).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um usuário cadastrado com este e-mail.",
        )

    novo_usuario = Usuario(
        nome=dados.nome.strip(),
        email=email_normalizado,
        senha_hash=gerar_hash_senha(dados.senha),
        perfil=PerfilUsuario.USUARIO,
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario


def garantir_admin_inicial(db: Session) -> None:
    admin_email = os.getenv("ADMIN_INIT_EMAIL", "").strip().lower()
    admin_senha = os.getenv("ADMIN_INIT_SENHA", "")
    admin_nome = os.getenv("ADMIN_INIT_NOME", "Administrador Inicial").strip()

    if not admin_email or not admin_senha:
        return

    existente = db.query(Usuario).filter(Usuario.email == admin_email).first()
    if existente:
        return

    admin = Usuario(
        nome=admin_nome,
        email=admin_email,
        senha_hash=gerar_hash_senha(admin_senha),
        perfil=PerfilUsuario.ADMINISTRADOR,
    )
    db.add(admin)
    db.commit()
