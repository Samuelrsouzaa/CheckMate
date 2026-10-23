from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import auth, checklists, tasks, tags, dashboard

# ==============================================================================
# O MOTOR DO BACKEND (app/main.py)
# ==============================================================================
# Quando nós damos o comando para ligar o servidor, o Python procura este arquivo.
# O objetivo principal deste arquivo NÃO é fazer contas ou salvar no banco,
# mas sim "Conectar os Fios". Ele é a placa-mãe do projeto.

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API for CheckMate, a productivity application with intelligent checklists."
)

# -----------------------------------------------------------------------------
# SEGURANÇA E COMUNICAÇÃO (CORS Middleware)
# -----------------------------------------------------------------------------
# CORS é a política que bloqueia sites desconhecidos de acessarem o nosso servidor.
# Como o nosso Frontend (HTML) roda em uma porta diferente do Backend (FastAPI),
# nós usamos o código abaixo para dizer ao navegador: "Fique tranquilo, nós permitimos 
# que o nosso frontend acesse este servidor".
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção colocaríamos apenas o link oficial do nosso site
    allow_credentials=True,
    allow_methods=["*"],  # Permite métodos HTTP como GET, POST, PUT, DELETE
    allow_headers=["*"],
)

# -----------------------------------------------------------------------------
# CONECTANDO OS ROTEADORES (APIs)
# -----------------------------------------------------------------------------
# Para não ficar um código de 5.000 linhas, nós separamos as URLs em outros arquivos.
# Ex: Se a requisição chegou em "/api/auth", o FastAPI automaticamente redireciona 
# o trabalho para o arquivo `auth.py` fazer a sua mágica.
app.include_router(auth.router, prefix="/api")
app.include_router(checklists.router, prefix="/api")
app.include_router(tasks.router, prefix="/api")
app.include_router(tags.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to CheckMate API. Visit /docs for Swagger UI."}
def root():
    return {"message": "Welcome to CheckMate API. Visit /docs for Swagger UI."}
