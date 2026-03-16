import sqlite3

with sqlite3.connect("db.sqlite3") as conn:
    conn.executescript("""
    PRAGMA foreign_keys = ON;

    CREATE TABLE IF NOT EXISTS turmas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ano INTEGER,
        turma TEXT,
        UNIQUE(ano,turma)
    );

    CREATE TABLE IF NOT EXISTS jogos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS sessoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        turma_id INTEGER NOT NULL,
        jogo_id INTEGER NOT NULL,
        palavra TEXT,
        dificuldade TEXT,
        tempo_total REAL,
        acertos INTEGER,
        erros INTEGER,
        pontuacao INTEGER,
        data_execucao DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (turma_id) REFERENCES turmas(id) ON DELETE CASCADE,
        FOREIGN KEY (jogo_id) REFERENCES jogos(id) ON DELETE CASCADE
    );
    """)
