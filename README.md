# CheckMate: API de Checklists e Produtividade

[![CI](https://github.com/Samuelrsouzaa/CheckMate/actions/workflows/ci.yml/badge.svg)](https://github.com/Samuelrsouzaa/CheckMate/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **English summary:** CheckMate is a containerized REST API (Python, FastAPI, PostgreSQL) with JWT authentication, Alembic migrations and an automated pytest suite, plus a vanilla JS web client. It lets students organize their studies with checklists and tasks. Built solo as a university project; used regularly by a real user.

Aplicação web para **estudantes organizarem seus estudos** com checklists e tarefas. É composta por uma **API REST** (Python/FastAPI) e um **cliente web** em HTML, CSS e JavaScript puro.

Projeto individual, desenvolvido na graduação em Ciência da Computação (CEUB). Usei ferramentas de IA como apoio durante o desenvolvimento, e revisei e entendi o código que integrei.

---

## Funcionalidades

- **Autenticação e segurança:** cadastro e login com **OAuth2 + JWT**; senhas armazenadas com hash **Bcrypt**; validação de e-mail e tamanho mínimo de senha (8 caracteres).
- **Isolamento de dados:** cada usuário só acessa os próprios checklists, tarefas e tags. Tentativas de acessar dados de outro usuário retornam `404`.
- **Checklists e tarefas:** CRUD completo, prioridade (`HIGH`, `MED`, `LOW`), status (`PENDING`, `DONE`, `LATE`) e data limite.
- **Tags:** criação e listagem de tags personalizadas.
- **Dashboard:** métricas de tarefas totais, concluídas, pendentes e atrasadas.
- **Documentação interativa:** Swagger UI e ReDoc gerados automaticamente pelo FastAPI.

### Regras de negócio implementadas
| Regra | Comportamento |
|---|---|
| Limite por conta | No máximo 50 checklists ativos (`403` ao exceder) |
| Exclusão de checklist | Bloqueada enquanto houver tarefas pendentes (`400`) |
| Exclusão de tarefa | *Soft delete*: a tarefa recebe `deletedAt` e some das listagens |
| Conclusão de tarefa | Ao marcar como `DONE`, o `completedAt` é preenchido |
| Título de tarefa | Mínimo de 3 caracteres (`422`) |

---

## Endpoints

Todos os endpoints, exceto `register` e `login`, exigem o header `Authorization: Bearer <token>`.

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/api/auth/register` | Cria uma conta |
| `POST` | `/api/auth/login` | Autentica e retorna o token JWT |
| `GET` | `/api/checklists/` | Lista os checklists do usuário |
| `POST` | `/api/checklists/` | Cria um checklist |
| `PUT` | `/api/checklists/{id}` | Atualiza ou arquiva um checklist |
| `DELETE` | `/api/checklists/{id}` | Remove um checklist |
| `GET` | `/api/tasks/checklist/{id}` | Lista as tarefas de um checklist |
| `POST` | `/api/tasks/` | Cria uma tarefa |
| `PUT` | `/api/tasks/{id}` | Atualiza uma tarefa (inclusive o status) |
| `DELETE` | `/api/tasks/{id}` | Move a tarefa para a lixeira |
| `GET` | `/api/tags/` | Lista as tags do usuário |
| `POST` | `/api/tags/` | Cria uma tag |
| `GET` | `/api/dashboard/` | Retorna as métricas de tarefas |

---

## Arquitetura

O código é dividido em camadas, com cada uma cuidando de uma responsabilidade:

```
app/
├── api/        # Camada de apresentação: rotas REST e injeção de dependências (FastAPI)
├── core/       # Configurações, segurança, hash de senha e tokens JWT
├── db/         # Engine e sessão do banco de dados
├── models/     # Modelos ORM (SQLAlchemy)
├── schemas/    # Schemas Pydantic (validação de entrada e saída)
└── services/   # Regras de negócio
alembic/        # Migrations do banco de dados
frontend/       # Cliente web (HTML, CSS e JavaScript puro)
tests/          # Testes automatizados (pytest)
```

## Stack

| Camada | Tecnologias |
|---|---|
| Back-end | Python 3.10, FastAPI, Pydantic v2 |
| Banco de dados | PostgreSQL, SQLAlchemy, Alembic |
| Segurança | JWT (PyJWT), Bcrypt (passlib), OAuth2 |
| Infraestrutura | Docker, Docker Compose, Adminer |
| Testes e CI | pytest, GitHub Actions |
| Front-end | HTML5, CSS3, JavaScript (Fetch API) |

---

## Como executar

### Pré-requisitos
[Docker Desktop](https://www.docker.com/products/docker-desktop/) e [Git](https://git-scm.com/).

### 1. Clonar e configurar
```bash
git clone https://github.com/Samuelrsouzaa/CheckMate.git
cd CheckMate
cp .env.example .env   # no Windows (PowerShell): Copy-Item .env.example .env
```
Edite o `.env` e troque a senha do banco e a `SECRET_KEY`. Sem o `.env`, o Compose usa valores padrão **apenas para desenvolvimento**.

### 2. Subir os serviços
```bash
docker compose up -d --build
docker compose exec api alembic upgrade head
```

| Serviço | URL |
|---|---|
| API e Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| Adminer (admin do banco) | http://localhost:8080 |
| Cliente web | abra `frontend/index.html` no navegador |

No Adminer, use o sistema **PostgreSQL**, o servidor `db` e as credenciais definidas no seu `.env`.

---

## Testes

A suíte tem **25 testes automatizados** e roda em um banco SQLite em memória, isolado do PostgreSQL. Eles cobrem:

- autenticação, tokens inválidos e senhas armazenadas como hash Bcrypt;
- isolamento de dados entre usuários;
- CRUD de checklists, tarefas e tags;
- regras de negócio e métricas do dashboard.

```bash
# Com Docker
docker compose exec api pytest -v

# Ou localmente
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
pytest -v
```

O GitHub Actions executa a mesma suíte a cada push e pull request.

---

## Variáveis de ambiente

| Variável | Descrição | Padrão (dev) |
|---|---|---|
| `DATABASE_URL` | String de conexão do banco | SQLite local |
| `SECRET_KEY` | Chave de assinatura do JWT | valor de desenvolvimento |
| `ALGORITHM` | Algoritmo do JWT | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Validade do token | `1440` |
| `CORS_ORIGINS` | Origens permitidas, separadas por vírgula | `*` |

> Em produção, defina uma `SECRET_KEY` forte e limite o `CORS_ORIGINS` ao domínio do front-end.

---

## Próximos passos

- [ ] Notificações e lembretes de prazo (a tabela `notifications` já existe no modelo)
- [ ] Registro de ações críticas em `audit_logs` (tabela já modelada)
- [ ] Atualização automática do status `LATE` para tarefas vencidas
- [ ] Limite de tentativas de login (*rate limiting*)
- [ ] Deploy online com HTTPS
- [ ] Interface em React

---

## Autor

**Samuel Souza**, estudante de Ciência da Computação (CEUB)

- GitHub: [@Samuelrsouzaa](https://github.com/Samuelrsouzaa)
- E-mail: [samuelrsouzasnt@gmail.com](mailto:samuelrsouzasnt@gmail.com)

Licença [MIT](LICENSE).
