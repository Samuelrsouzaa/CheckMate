"""Testes de regras de negocio: checklists, tarefas, tags e dashboard."""


def _create_checklist(client, headers, name="My List"):
    response = client.post("/api/checklists/", json={"name": name}, headers=headers)
    assert response.status_code == 201
    return response.json()


def _create_task(client, headers, checklist_id, title="My Task"):
    response = client.post(
        "/api/tasks/", json={"checklistId": checklist_id, "title": title}, headers=headers
    )
    assert response.status_code == 201
    return response.json()


def test_checklist_crud_flow(client, auth_headers):
    checklist = _create_checklist(client, auth_headers, "Estudos")
    assert checklist["name"] == "Estudos"
    assert checklist["isArchived"] is False

    updated = client.put(
        f"/api/checklists/{checklist['id']}",
        json={"name": "Estudos 2026", "isArchived": True},
        headers=auth_headers,
    )
    assert updated.status_code == 200
    assert updated.json()["name"] == "Estudos 2026"
    assert updated.json()["isArchived"] is True

    deleted = client.delete(f"/api/checklists/{checklist['id']}", headers=auth_headers)
    assert deleted.status_code == 200
    assert client.get("/api/checklists/", headers=auth_headers).json() == []


def test_cannot_delete_checklist_with_pending_tasks(client, auth_headers):
    checklist = _create_checklist(client, auth_headers)
    _create_task(client, auth_headers, checklist["id"])

    response = client.delete(f"/api/checklists/{checklist['id']}", headers=auth_headers)
    assert response.status_code == 400


def test_can_delete_checklist_after_tasks_are_completed(client, auth_headers):
    checklist = _create_checklist(client, auth_headers)
    task = _create_task(client, auth_headers, checklist["id"])
    client.put(f"/api/tasks/{task['id']}", json={"status": "DONE"}, headers=auth_headers)

    response = client.delete(f"/api/checklists/{checklist['id']}", headers=auth_headers)
    assert response.status_code == 200


def test_checklist_limit_for_free_accounts(client, auth_headers):
    for index in range(50):
        _create_checklist(client, auth_headers, f"List {index}")

    response = client.post("/api/checklists/", json={"name": "One too many"}, headers=auth_headers)
    assert response.status_code == 403


def test_completing_task_sets_completed_at(client, auth_headers):
    checklist = _create_checklist(client, auth_headers)
    task = _create_task(client, auth_headers, checklist["id"])
    assert task["status"] == "PENDING"
    assert task["completedAt"] is None

    response = client.put(f"/api/tasks/{task['id']}", json={"status": "DONE"}, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["status"] == "DONE"
    assert response.json()["completedAt"] is not None


def test_deleted_task_is_hidden_from_listing(client, auth_headers):
    checklist = _create_checklist(client, auth_headers)
    task = _create_task(client, auth_headers, checklist["id"])
    client.delete(f"/api/tasks/{task['id']}", headers=auth_headers)

    tasks = client.get(f"/api/tasks/checklist/{checklist['id']}", headers=auth_headers).json()
    assert tasks == []


def test_update_unknown_task_returns_404(client, auth_headers):
    response = client.put("/api/tasks/99999", json={"title": "Ghost"}, headers=auth_headers)
    assert response.status_code == 404


def test_tags_create_and_list(client, auth_headers):
    created = client.post("/api/tags/", json={"name": "urgente", "color": "#ff0000"}, headers=auth_headers)
    assert created.status_code == 200
    assert created.json()["name"] == "urgente"

    tags = client.get("/api/tags/", headers=auth_headers).json()
    assert [tag["name"] for tag in tags] == ["urgente"]


def test_dashboard_metrics_reflect_task_status(client, auth_headers):
    checklist = _create_checklist(client, auth_headers)
    done_task = _create_task(client, auth_headers, checklist["id"], "Task one")
    _create_task(client, auth_headers, checklist["id"], "Task two")
    removed_task = _create_task(client, auth_headers, checklist["id"], "Task three")

    client.put(f"/api/tasks/{done_task['id']}", json={"status": "DONE"}, headers=auth_headers)
    client.delete(f"/api/tasks/{removed_task['id']}", headers=auth_headers)

    metrics = client.get("/api/dashboard/", headers=auth_headers).json()
    assert metrics["total_tasks"] == 2
    assert metrics["completed_tasks"] == 1
    assert metrics["pending_tasks"] == 1
    assert metrics["late_tasks"] == 0
