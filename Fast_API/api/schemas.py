from pydantic import BaseModel
from typing import Optional


# ------------------------
# TURMAS
# ------------------------

class TurmasCreate(BaseModel):
    ano: int
    turma: str


# ------------------------
# JOGOS
# ------------------------

class JogosCreate(BaseModel):
    nome: str


# ------------------------
# ALUNOS
# ------------------------

class AlunosCreate(BaseModel):
    ra: str
    nome: str
    turma_id: int


# ------------------------
# SESSOES
# ------------------------

class SessoesCreate(BaseModel):
    aluno_id: int
    jogo_id: int
    palavra: Optional[str] = None
    dificuldade: Optional[str] = None
    tempo_total: Optional[float] = None
    acertos: Optional[int] = None
    erros: Optional[int] = None
    pontuacao: Optional[int] = None


# ------------------------
# SESSOES CLIENT (recebe dados do jogo)
# ------------------------
class SessoesClientCreate(BaseModel):
    ra: str
    nome: str
    turma: str
    jogo: str
    dificuldade: Optional[str] = None
    palavra: Optional[str] = None
    tempo_total: Optional[float] = None
    acertos: Optional[int] = None
    erros: Optional[int] = None
    pontuacao: Optional[int] = None
