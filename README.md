# CheckMate ♟️ - Smart Checklist & Productivity API

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A robust, containerized RESTful API and productivity tool built for task and checklist management. Engineered with **Clean Architecture**, automated testing, database migrations, and a clean web interface.

> 🎓 **Academic Context**: This application was developed as a comprehensive practical final project for university coursework in software engineering and web backend development. It was designed to demonstrate industry-standard software design patterns, end-to-end containerization, authentication security, relational database design, and unit/integration testing.

---

## 🎯 Features

- **Authentication & Security**: User registration, login, and token-based authentication using **OAuth2 with JWT (JSON Web Tokens)** and **Bcrypt** password hashing.
- **Task & Checklist Management**: Full CRUD operations for checklists and sub-tasks with status toggles, prioritization, and categorization.
- **Tagging & Filtering**: Organize tasks and checklists with custom tags for productivity tracking.
- **Dashboard & Metrics**: Dedicated dashboard endpoints delivering real-time statistics on completed vs. pending tasks.
- **Audit Logging**: System audit logs recording critical user actions.
- **Interactive Documentation**: Auto-generated OpenAPI / Swagger UI and ReDoc interfaces.
- **Frontend Dashboard**: Responsive web client for interacting with the API in real time.

---

## 🏗️ Architecture & Design Patterns

The codebase strictly follows **Clean Architecture** and separation of concerns:

```
app/
├── api/          # Presentation Layer: REST endpoints, routing, dependency injection (FastAPI)
├── core/         # Core Configurations: Security, JWT tokens, environment settings
├── db/           # Infrastructure: Database engine session, connection pool
├── models/       # Domain Layer: SQLAlchemy ORM database models
├── schemas/      # Application Layer: Pydantic schemas (DTOs & payload validation)
└── services/     # Business Logic Layer: Service classes and domain use cases
```

---

## 🛠️ Tech Stack

- **Backend**: Python 3.11, [FastAPI](https://fastapi.tiangolo.com/), [Pydantic v2](https://docs.pydantic.dev/)
- **Database & ORM**: PostgreSQL, [SQLAlchemy](https://www.sqlalchemy.org/), [Alembic](https://alembic.sqlalchemy.org/) (Migrations)
- **Containerization**: Docker, Docker Compose
- **Testing**: [pytest](https://docs.pytest.org/), SQLite (isolated in-memory test database)
- **Database Management Tool**: Adminer
- **Frontend**: HTML5, Modern CSS3, JavaScript (Fetch API)

---

## 🚀 Getting Started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
- [Git](https://git-scm.com/) installed.

### 1. Clone the repository
```bash
git clone https://github.com/Samuelrsouzaa/CheckMate.git
cd CheckMate
```

### 2. Run with Docker Compose
Spin up the entire application stack (API server, PostgreSQL database, and Adminer):
```bash
docker-compose up -d --build
```

### 3. Run Database Migrations
Apply the initial database schema using Alembic:
```bash
docker-compose exec api alembic upgrade head
```

The services will be available at:
- **API & Live Documentation (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Alternative Documentation (ReDoc)**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Database Web Admin (Adminer)**: [http://localhost:8080](http://localhost:8080)
- **Web Frontend**: Open `frontend/index.html` in your web browser.

---

## 🧪 Running Automated Tests

The automated test suite runs against an isolated, high-performance in-memory SQLite database (`sqlite:///:memory:`):

```bash
docker-compose exec api pytest -v
```

---

## 🗄️ Database Management (Adminer)

To inspect database records directly via the Adminer UI at `http://localhost:8080`:
- **System**: PostgreSQL
- **Server**: `db`
- **Username**: `checkmate_user`
- **Password**: `checkmate_pass`
- **Database**: `checkmate_db`

---

## 👤 Author

Developed by **Samuel Souza** and project partner as an academic capstone/practical project.

- GitHub: [@Samuelrsouzaa](https://github.com/Samuelrsouzaa)
- Email: [samuelrsouzasnt@gmail.com](mailto:samuelrsouzasnt@gmail.com)
