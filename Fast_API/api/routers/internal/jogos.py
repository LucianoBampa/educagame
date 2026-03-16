#ENDPOINTS DE JOGOS
from fastapi import APIRouter, Depends
from ...services import jogos_services
from ... import schemas
from ...database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/jogos",
    tags=["Internal"]
)
@router.get("/")
def get_jogos(db: Session = Depends(get_db)):
    return jogos_services.listar_jogo(db)

@router.post("/")
def post_jogo(jogo:schemas.JogosCreate, db: Session = Depends(get_db)):
    return jogos_services.criar_jogo(db, jogo.nome)

@router.delete("/{jogo_id}")
def delete_jogo(jogo_id: int, db: Session = Depends(get_db)):
    return jogos_services.deletar_jogo(db, jogo_id)
