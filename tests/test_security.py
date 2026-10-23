"""Testes de autenticacao, autorizacao e isolamento de dados entre usuarios."""
from app.models.user import User


def _register_and_login(client, email="other@example.com", password="OtherPass1!"):
    response = client.post(
        "/api/auth/register",
        json={"name": "Other User", "email": email, "password": password},
    )
    assert response.status_code == 201
    login = client.post("/api/auth/login", data={"username": email, "password": password})
    assert login.status_code == 200
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def test_register_success_does_not_expose_password(client):
    response = client.post(
        "/api/auth/register",
        json={"name": "New User", "email": "new@example.com", "password": "StrongPass1!"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "new@example.com"
    assert "password" not in body
    assert "passwordHash" not in body


def test_password_is_stored_as_bcrypt_hash(client, db):
    client.post(
        "/api/auth/register",
        json={"name": "Hash User", "email": "hash@example.com", "password": "StrongPass1!"},
    )
    user = db.query(User).filter(User.email == "hash@example.com").first()
    assert user is not None
    assert user.passwordHash != "StrongPass1!"
    assert user.passwordHash.startswith("$2")


def test_register_duplicate_email_is_rejected(client):
    response = client.post(
        "/api/auth/register",
        json={"name": "Dup", "email": "test@example.com", "password": "StrongPass1!"},
    )
    assert response.status_code == 400


def test_register_invalid_email_is_rejected(client):
    response = client.post(
        "/api/auth/register",
        json={"name": "Bad Email", "email": "not-an-email", "password": "StrongPass1!"},
    )
    assert response.status_code == 422


def test_login_wrong_password_returns_401(client):
    response = client.post(
        "/api/auth/login",
        data={"username": "test@example.com", "password": "WrongPass1!"},
    )
    assert response.status_code == 401


def test_login_unknown_user_returns_401(client):
    response = client.post(
        "/api/auth/login",
        data={"username": "ghost@example.com", "password": "StrongPass1!"},
    )
    assert response.status_code == 401


def test_protected_routes_require_token(client):
    for path in ("/api/checklists/", "/api/tags/", "/api/dashboard/"):
        assert client.get(path).status_code == 401


def test_invalid_token_is_rejected(client):
    response = client.get("/api/checklists/", headers={"Authorization": "Bearer token.invalido.aqui"})
    assert response.status_code == 401


def test_user_cannot_read_another_users_tasks(client, auth_headers):
    checklist = client.post("/api/checklists/", json={"name": "Private"}, headers=auth_headers).json()
    other_headers = _register_and_login(client)

    response = client.get(f"/api/tasks/checklist/{checklist['id']}", headers=other_headers)
    assert response.status_code == 404


def test_user_cannot_create_task_in_another_users_checklist(client, auth_headers):
    checklist = client.post("/api/checklists/", json={"name": "Private"}, headers=auth_headers).json()
    other_headers = _register_and_login(client)

    response = client.post(
        "/api/tasks/",
        json={"checklistId": checklist["id"], "title": "Intruder task"},
        headers=other_headers,
    )
    assert response.status_code == 404


def test_user_cannot_update_or_delete_another_users_checklist(client, auth_headers):
    checklist = client.post("/api/checklists/", json={"name": "Private"}, headers=auth_headers).json()
    other_headers = _register_and_login(client)

    update = client.put(f"/api/checklists/{checklist['id']}", json={"name": "Hacked"}, headers=other_headers)
    delete = client.delete(f"/api/checklists/{checklist['id']}", headers=other_headers)
    assert update.status_code == 404
    assert delete.status_code == 404


def test_checklist_list_only_returns_own_data(client, auth_headers):
    client.post("/api/checklists/", json={"name": "Mine"}, headers=auth_headers)
    other_headers = _register_and_login(client)

    assert client.get("/api/checklists/", headers=other_headers).json() == []
    assert len(client.get("/api/checklists/", headers=auth_headers).json()) == 1
