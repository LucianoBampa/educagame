# FastAPI Escola

API simples para gerenciamento de turmas, jogos e sessões.

## Estrutura do Projeto
```
├── main.py           # aplicação FastAPI principal
├── models.py         # modelos do SQLAlchemy
├── schemas.py        # Pydantic schemas
├── services.py       # funções de negócio
├── create_db.py      # cria o banco de dados
├── populate_db.py    # popula dados iniciais
├── requirements.txt  # dependências
├── .env              # variáveis de ambiente (ex.: API_SENHA_GERAL)
├── db.sqlite3        # banco SQLite
└── venv/             # ambiente virtual
```
## Configuração

1. Criar e ativar ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
```

2. Instalar Dependências 
```
pip install -r requirements.txt
```
3. Criar banco de dados e (opcional) popular
```
python scripts/create_db.py
python scripts/populate_db.py
```
4. Crie .env e configure como em .env.example
```
#.env file
API_KEY=""
DATABASE_URL="sqlite:///./db.sqlite3"
```
5. Rodar com
```
uvicorn api.main:app --reload
```
Documentação automática do FastAPI disponivel em localhost:8000/docs




