import os
from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func, UniqueConstraint
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)



class Base(DeclarativeBase):
    pass

class AlunosModel(Base):
    __tablename__ = "alunos"

    id: Mapped[int] = mapped_column(primary_key=True)
    ra: Mapped[str] = mapped_column(String, unique=True, index=True)
    nome: Mapped[str] = mapped_column(String)

    turma_id: Mapped[int] = mapped_column(ForeignKey("turmas.id"))

    # relacionamento
    turma = relationship("TurmasModel", back_populates="alunos")
    sessoes = relationship("SessoesModel", back_populates="aluno")

class TurmasModel(Base):
    __tablename__ = "turmas"
    __table_args__ = (
        UniqueConstraint("ano", "turma", name="uq_ano_turma"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    ano: Mapped[int] = mapped_column(Integer, nullable=True)
    turma: Mapped[str] = mapped_column(String, nullable=True)
    alunos = relationship("AlunosModel", back_populates="turma")
    
class JogosModel(Base):
    __tablename__ = "jogos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    sessoes: Mapped[List["SessoesModel"]] = relationship(
        back_populates="jogo",
        cascade="all, delete",
    )


class SessoesModel(Base):
    __tablename__ = "sessoes"

    id: Mapped[int] = mapped_column(primary_key=True)

    aluno_id: Mapped[int] = mapped_column(ForeignKey("alunos.id"))

    aluno = relationship("AlunosModel", back_populates="sessoes")

    jogo_id: Mapped[int] = mapped_column(ForeignKey("jogos.id", ondelete="CASCADE"))

    palavra: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    dificuldade: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    tempo_total: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    acertos: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    erros: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    pontuacao: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    data_execucao: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )

    jogo: Mapped["JogosModel"] = relationship(back_populates="sessoes")

