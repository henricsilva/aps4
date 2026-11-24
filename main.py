from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

from controller import auth_controller, usuario_controller
from database import Base, SessionLocal, engine
import model.usuario  # Garante o registro do modelo Usuario no metadata
from service.usuario_service import garantir_admin_inicial


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        garantir_admin_inicial(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="API de Eventos Acadêmicos",
    description="API RESTful com autenticação JWT, controle de acesso por perfil e relatórios.",
    version="4.0.0",
    lifespan=lifespan,
)

app.include_router(usuario_controller.router)
app.include_router(auth_controller.router)
