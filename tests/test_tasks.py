from app.extensions import db
from app.models import Task
from tests.conftest import auth_header, create_user, login


def test_user_can_create_list_update_and_delete_own_task(client):
    create_user()
    token = login(client)

    create_response = client.post(
        "/api/tasks",
        headers=auth_header(token),
        json={"title": "Finish API", "priority": "high", "due_date": "2026-06-01"},
    )

    assert create_response.status_code == 201
    task = create_response.get_json()["task"]
    assert task["title"] == "Finish API"
    assert task["status"] == "todo"

    list_response = client.get("/api/tasks", headers=auth_header(token))
    assert list_response.status_code == 200
    assert len(list_response.get_json()["tasks"]) == 1

    update_response = client.patch(
        f"/api/tasks/{task['id']}",
        headers=auth_header(token),
        json={"status": "done"},
    )
    assert update_response.status_code == 200
    assert update_response.get_json()["task"]["status"] == "done"

    delete_response = client.delete(f"/api/tasks/{task['id']}", headers=auth_header(token))
    assert delete_response.status_code == 204

    list_after_delete = client.get("/api/tasks", headers=auth_header(token))
    assert list_after_delete.get_json()["tasks"] == []


def test_user_cannot_access_another_users_task(client):
    owner = create_user(username="owner", email="owner@example.com")
    outsider = create_user(username="outsider", email="outsider@example.com")
    task = Task(title="Private task", owner_id=owner.id)
    db.session.add(task)
    db.session.commit()

    token = login(client, email=outsider.email)

    response = client.get(f"/api/tasks/{task.id}", headers=auth_header(token))

    assert response.status_code == 403


def test_admin_can_access_all_tasks(client):
    user = create_user(username="owner", email="owner@example.com")
    admin = create_user(username="admin", email="admin@example.com", role="admin")
    task = Task(title="Visible to admin", owner_id=user.id)
    db.session.add(task)
    db.session.commit()

    token = login(client, email=admin.email)

    list_response = client.get("/api/tasks", headers=auth_header(token))
    detail_response = client.get(f"/api/tasks/{task.id}", headers=auth_header(token))

    assert list_response.status_code == 200
    assert len(list_response.get_json()["tasks"]) == 1
    assert detail_response.status_code == 200
    assert detail_response.get_json()["task"]["title"] == "Visible to admin"


def test_task_validation_rejects_invalid_status(client):
    create_user()
    token = login(client)

    response = client.post(
        "/api/tasks",
        headers=auth_header(token),
        json={"title": "Bad status", "status": "blocked"},
    )

    assert response.status_code == 400
    assert "status" in response.get_json()["errors"]
