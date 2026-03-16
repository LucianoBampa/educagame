from fastapi import APIRouter, Depends
from ...services import sessoes_services
from ... import schemas
from ...database import get_db
from ...models import AlunosModel, JogosModel, TurmasModel
from sqlalchemy.orm import Session
from datetime import datetime

router = APIRouter(
    prefix="/sessoes",
    tags=["Client"]
)

@router.post("/")
def post_sessoes(sessao: schemas.SessoesClientCreate, db: Session = Depends(get_db)):
    ano_letivo = datetime.now().year

    # Busca ou cria o jogo
    jogo = db.query(JogosModel).filter(JogosModel.nome == sessao.jogo).first()
    if not jogo:
        jogo = JogosModel(nome=sessao.jogo)
        db.add(jogo)
        db.commit()
        db.refresh(jogo)

    # Busca ou cria a turma (ex: "3B" + 2026)
    turma = db.query(TurmasModel).filter(
        TurmasModel.turma == sessao.turma.strip().upper(),
        TurmasModel.ano == ano_letivo
    ).first()
    if not turma:
        turma = TurmasModel(ano=ano_letivo, turma=sessao.turma.strip().upper())
        db.add(turma)
        db.commit()
        db.refresh(turma)

    # Busca ou cria o aluno
    aluno = db.query(AlunosModel).filter(AlunosModel.ra == sessao.ra).first()
    if not aluno:
        aluno = AlunosModel(ra=sessao.ra, nome=sessao.nome, turma_id=turma.id)
        db.add(aluno)
        db.commit()
        db.refresh(aluno)

    # Cria a sessão
    dados = schemas.SessoesCreate(
        aluno_id=aluno.id,
        jogo_id=jogo.id,
        palavra=sessao.palavra,
        dificuldade=sessao.dificuldade,
        tempo_total=sessao.tempo_total,
        acertos=sessao.acertos,
        erros=sessao.erros,
        pontuacao=sessao.pontuacao,

    )
    return sessoes_services.criar_sessao(db, dados)