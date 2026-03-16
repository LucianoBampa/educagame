from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine, get_db
from .config import API_KEY

#ROUTERS INTERNOS
from .routers.internal.jogos import router as internal_jogos
from .routers.internal.turmas import router as internal_turmas
from .routers.internal.sessoes import router as internal_sessoes
from .routers.internal.alunos import router as internal_alunos
#ROUTERS CLIENTS
from .routers.client.jogos import router as client_jogos
from .routers.client.turmas import router as client_turmas
from .routers.client.sessoes import router as client_sessoes

Base.metadata.create_all(bind=engine)
app = FastAPI()

# CORS - permite requisições do jogo local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def validar_api_key(x_api_key: str = Header(alias="X-API-Key")):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401)

def validar_internal(request: Request):
    if request.client is None:
        raise HTTPException(status_code=401)
    if request.client.host != "127.0.0.1":
        raise HTTPException(status_code=401)

# --------------------------
# Routers Internos
# --------------------------
internal_router = APIRouter(prefix="/api/internal", dependencies=[Depends(validar_internal)])
internal_router.include_router(internal_jogos)
internal_router.include_router(internal_turmas)
internal_router.include_router(internal_sessoes)
internal_router.include_router(internal_alunos)
app.include_router(internal_router)

@app.get("/api/internal/health", tags=["Internal"])
def health(_: None = Depends(validar_internal)):
    return {"ok": True}

# --------------------------
# Routers Client (sem API Key)
# --------------------------
client_router = APIRouter(prefix="/api/client")
client_router.include_router(client_jogos)
client_router.include_router(client_turmas)
client_router.include_router(client_sessoes)
app.include_router(client_router)