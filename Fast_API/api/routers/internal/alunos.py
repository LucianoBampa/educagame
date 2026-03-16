from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.database import get_db
from api import models, schemas

router = APIRouter(prefix="/alunos", tags=["Internal - Alunos"])


# ------------------------
# LISTAR ALUNOS
# ------------------------
@router.get("/")
def listar_alunos(db: Session = Depends(get_db)):
    return db.query(models.AlunosModel).all()


# ------------------------
# CRIAR ALUNO
# ------------------------
@router.post("/")
def criar_aluno(aluno: schemas.AlunosCreate, db: Session = Depends(get_db)):

    # verificar se RA já existe
    aluno_existente = (
        db.query(models.AlunosModel)
        .filter(models.AlunosModel.ra == aluno.ra)
        .first()
    )

    if aluno_existente:
        raise HTTPException(status_code=400, detail="RA já cadastrado")

    novo_aluno = models.AlunosModel(
        ra=aluno.ra,
        nome=aluno.nome,
        turma_id=aluno.turma_id,
    )

    db.add(novo_aluno)
    db.commit()
    db.refresh(novo_aluno)

    return novo_aluno


# ------------------------
# DELETAR ALUNO
# ------------------------
@router.delete("/{aluno_id}")
def deletar_aluno(aluno_id: int, db: Session = Depends(get_db)):

    aluno = db.query(models.AlunosModel).get(aluno_id)

    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    db.delete(aluno)
    db.commit()

    return {"message": "Aluno deletado com sucesso"}
