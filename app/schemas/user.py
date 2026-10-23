from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# ==============================================================================
# SCHEMAS DE USUÁRIO (app/schemas/user.py)
# ==============================================================================
# Esta camada é o nosso "Avaliador de Qualidade". 
# Usamos a biblioteca Pydantic para validar os JSONs que chegam da internet.
# Se um hacker tentar enviar um e-mail falso ("teste@"), o Pydantic vai bloquear.

class UserBase(BaseModel):
    name: str
    email: EmailStr  # O Pydantic valida sozinho se tem '@' e '.com'

# Herda o UserBase, ou seja, tem nome e e-mail, e adiciona a SENHA.
# Usado APENAS quando o usuário está criando a conta (Recebendo do Frontend).
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="A senha deve ter pelo menos 8 caracteres")

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserOut(UserBase):
    id: int
    role: str
    isActive: bool
    createdAt: datetime
    lastLoginAt: Optional[datetime] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
