from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

# ==============================================================================
# OS SERVIÇOS DO USUÁRIO (app/services/user.py)
# ==============================================================================
# Bem-vindo à "Cozinha" do nosso restaurante (Clean Architecture)!
# O arquivo de rotas (auth.py) recebe os pedidos do cliente e repassa para cá.
# Este é o ÚNICO lugar que tem permissão para manipular o Banco de Dados.

def get_user_by_email(db: Session, email: str):
    # ORM na prática: Usamos Python para buscar dados em vez de escrever SQL puro.
    # O SQLAlchemy traduz isso para: "SELECT * FROM users WHERE email = ? LIMIT 1"
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    # 1. SEGURANÇA MÁXIMA: NUNCA salvamos a senha em texto limpo!
    # Passamos a senha pelo algoritmo Bcrypt (Hash Irreversível).
    # Ex: 'Senha123' vira '$2b$12$KIXpZ/pS5O7q...' (Se vazar, o hacker não lê nada)
    hashed_password = get_password_hash(user.password)
    
    # 2. Criamos a "Instância" do banco de dados (A linha da tabela)
    db_user = User(email=user.email, name=user.name, passwordHash=hashed_password)
    
    # 3. Adicionamos a linha na memória do SQLAlchemy
    db.add(db_user)
    
    # 4. COMMIT: Salva definitivamente no PostgreSQL
    db.commit()
    
    # 5. REFRESH: Puxa os dados de volta do banco para pegar o 'ID' automático
    db.refresh(db_user)
    
    return db_user
