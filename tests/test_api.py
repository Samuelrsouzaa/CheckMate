def test_ca01_register_weak_password(client):
    response = client.post(
        "/api/auth/register",
        json={"name": "New User", "email": "new@example.com", "password": "123"}
    )
    # A validacao do schema (Pydantic, min_length=8) rejeita a senha antes da regra manual da rota.
    assert response.status_code == 422
    assert "password" in response.text

def test_ca03_login_valid_credentials(client):
    response = client.post(
        "/api/auth/login",
        data={"username": "test@example.com", "password": "StrongPass1!"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_ca05_create_task_without_title(client, auth_headers):
    # Create checklist first
    cl_response = client.post("/api/checklists/", json={"name": "My List"}, headers=auth_headers)
    cl_id = cl_response.json()["id"]

    # Try creating task without title
    response = client.post(
        "/api/tasks/",
        json={"checklistId": cl_id, "title": "ab"}, # Title too short
        headers=auth_headers
    )
    assert response.status_code == 422

def test_ca08_delete_task_moves_to_trash(client, auth_headers):
    # Create checklist
    cl_response = client.post("/api/checklists/", json={"name": "My List"}, headers=auth_headers)
    cl_id = cl_response.json()["id"]

    # Create task
    task_response = client.post(
        "/api/tasks/",
        json={"checklistId": cl_id, "title": "My Task"},
        headers=auth_headers
    )
    task_id = task_response.json()["id"]

    # Delete task
    del_response = client.delete(f"/api/tasks/{task_id}", headers=auth_headers)
    assert del_response.status_code == 200
    
    # Verify deletedAt is not null
    deleted_task = del_response.json()
    assert deleted_task["deletedAt"] is not None
