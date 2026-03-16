from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from ..models import JogosModel


def listar_jogo(db:Session):
    return db.query(JogosModel).all()

def criar_jogo(db: Session, nome: str):
    novo = JogosModel(nome=nome)
    db.add(novo)
    try:
        db.commit()
        db.refresh(novo)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Jogo já existe")
    return novo


def deletar_jogo(db: Session, jogo_id: int):
    jogo = db.get(JogosModel, jogo_id)
    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")

    db.delete(jogo)
    db.commit()
    return {"detail": f"Jogo {jogo.nome} deletado com sucesso"}
