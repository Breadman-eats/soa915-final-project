from fastapi.testclient import TestClient
from main import app, users_db

client = TestClient(app)


def setup_function():
    """Reset the in-memory DB before each test so tests don't interfere with each other."""
    users_db.clear()


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "User Service is running"}


def test_create_user():
    response = client.post("/users", json={"name": "Alice", "email": "alice@example.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"
    assert "id" in data


def test_list_users_empty():
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == []


def test_list_users_after_create():
    client.post("/users", json={"name": "Bob", "email": "bob@example.com"})
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_user_success():
    created = client.post("/users", json={"name": "Carol", "email": "carol@example.com"}).json()
    response = client.get(f"/users/{created['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Carol"


def test_get_user_not_found():
    response = client.get("/users/999")
    assert response.status_code == 404


def test_delete_user_success():
    created = client.post("/users", json={"name": "Dan", "email": "dan@example.com"}).json()
    response = client.delete(f"/users/{created['id']}")
    assert response.status_code == 200
    # confirm it's actually gone
    get_response = client.get(f"/users/{created['id']}")
    assert get_response.status_code == 404


def test_delete_user_not_found():
    response = client.delete("/users/999")
    assert response.status_code == 404
