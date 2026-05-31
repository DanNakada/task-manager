
import pytest
import src.app as app_module
from src.app import app


@pytest.fixture(autouse=True)
def reset_state():
    app_module.state["tasks"].clear()
    app_module.state["next_id"] = 1
    yield
    app_module.state["tasks"].clear()
    app_module.state["next_id"] = 1


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_create_task_success(client):
    response = client.post("/tasks", json={"title": "Estudar Flask"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Estudar Flask"
    assert data["status"] == "pending"
    assert data["id"] == 1


def test_create_task_without_title(client):
    response = client.post("/tasks", json={"description": "Sem título"})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_create_task_empty_title(client):
    response = client.post("/tasks", json={"title": "   "})
    assert response.status_code == 400


def test_create_task_invalid_status(client):
    response = client.post("/tasks", json={"title": "Tarefa", "status": "invalido"})
    assert response.status_code == 400


def test_list_tasks_empty(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.get_json() == []


def test_list_tasks_returns_all(client):
    client.post("/tasks", json={"title": "Tarefa 1"})
    client.post("/tasks", json={"title": "Tarefa 2"})
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.get_json()) == 2


def test_filter_tasks_by_status_pending(client):
    client.post("/tasks", json={"title": "Pendente", "status": "pending"})
    client.post("/tasks", json={"title": "Concluida", "status": "done"})
    response = client.get("/tasks?status=pending")
    data = response.get_json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["status"] == "pending"


def test_filter_tasks_invalid_status(client):
    response = client.get("/tasks?status=invalido")
    assert response.status_code == 400


def test_update_task_success(client):
    client.post("/tasks", json={"title": "Tarefa original"})
    response = client.put("/tasks/1", json={"title": "Tarefa atualizada"})
    assert response.status_code == 200
    assert response.get_json()["title"] == "Tarefa atualizada"


def test_update_nonexistent_task(client):
    response = client.put("/tasks/999", json={"title": "Não existe"})
    assert response.status_code == 404


def test_delete_task_success(client):
    client.post("/tasks", json={"title": "Para deletar"})
    response = client.delete("/tasks/1")
    assert response.status_code == 200
    assert len(client.get("/tasks").get_json()) == 0


def test_delete_nonexistent_task(client):
    response = client.delete("/tasks/999")
    assert response.status_code == 404
