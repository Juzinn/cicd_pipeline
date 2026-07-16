import pytest
from app import app, tasks


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_get_all_tasks(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_create_task(client):
    response = client.post("/tasks", json={"title": "Test CI/CD pipeline"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Test CI/CD pipeline"
    assert data["done"] is False


def test_create_task_missing_title(client):
    response = client.post("/tasks", json={})
    assert response.status_code == 400


def test_get_single_task(client):
    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert response.get_json()["id"] == 1


def test_get_nonexistent_task(client):
    response = client.get("/tasks/9999")
    assert response.status_code == 404


def test_update_task(client):
    response = client.put("/tasks/1", json={"done": True})
    assert response.status_code == 200
    assert response.get_json()["done"] is True


def test_delete_task(client):
    response = client.delete("/tasks/2")
    assert response.status_code == 204

    # confirm it's actually gone
    response = client.get("/tasks/2")
    assert response.status_code == 404