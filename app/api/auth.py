from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.db.database import get_db
from app.schemas.user import UserCreate, UserOut, Token
from app.services.user import create_user, get_user_by_email

# ==============================================================================
# ROTEADOR DE AUTENTICAÇÃO (app/api/auth.py)
# ==============================================================================
# Este é o nosso "Balcão de Atendimento" para quem quer entrar no sistema.
# Só temos duas opções: ou a pessoa se cadastra (Register) ou ela entra (Login).

router = APIRouter(prefix="/auth", tags=["auth"])

# -----------------------------------------------------------------------------
# 1. ROTA DE REGISTRO (CRIAR CONTA)
# -----------------------------------------------------------------------------
# O frontend envia um JSON (nome, email, senha) e o Pydantic transforma na classe `UserCreate`.
# A palavra "Depends(get_db)" faz a Injeção de Dependências. Em vez de ficarmos conectados
# ao banco o tempo todo consumindo memória, o banco de dados só abre no milissegundo 
# em que essa função é disparada!
@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    
    # 1º Passo: Checar se já existe alguém no banco de dados com esse email.
    user = get_user_by_email(db, email=user_in.email)
    if user:
        # Se existir, encerramos a operação aqui e o servidor devolve um erro HTTP 400.
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
        
    # 2º Passo: Validar a força da senha (Exemplo de Regra de Negócio na API)
    if len(user_in.password) < 8:
        raise HTTPException(status_code=400, detail="Senha deve ter no mínimo 8 caracteres.")
        
    # 3º Passo: Chamar o "Cozinheiro" (Services) para de fato pegar esses ingredientes 
    # e criar o usuário lá na tabela do PostgreSQL.
    user = create_user(db, user_in)
    
    # Ao final, devolvemos a foto do usuário sem a senha (UserOut).
    return user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Basic rate limiting would be here (RNF08)
    user = get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.passwordHash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.email, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
