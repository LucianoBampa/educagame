from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from ..models import TurmasModel
from ..models import AlunosModel

def listar_turmas(db: Session):
    return db.query(TurmasModel).all()


def criar_turma(db: Session, turma: str, ano: int):
    nova = TurmasModel(turma=turma, ano=ano)
    db.add(nova)
    try:
        db.commit()
        db.refresh(nova)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Turma já existe")
    return nova


def deletar_turma(db: Session, turma_id: int):
    turma = db.get(TurmasModel, turma_id)
    if not turma:
        raise HTTPException(status_code=404, detail="Turma não encontrada")

    db.delete(turma)
    db.commit()
    return {"detail": f"Turma deletada [{turma.turma}] com sucesso."}

def listar_alunos_por_turma(db: Session, turma_id: int):
    return (
        db.query(AlunosModel)
        .filter(AlunosModel.turma_id == turma_id)
        .all()
    )
