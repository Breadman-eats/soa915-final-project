from fastapi.testclient import TestClient
from main import app, orders_db

client = TestClient(app)


def setup_function():
    """Reset the in-memory DB before each test so tests don't interfere with each other."""
    orders_db.clear()


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Order Service is running"}


def test_create_order():
    response = client.post("/orders", json={"user_id": 1, "item": "Laptop", "quantity": 2})
    assert response.status_code == 200
    data = response.json()
    assert data["item"] == "Laptop"
    assert data["quantity"] == 2
    assert data["status"] == "pending"
    assert "id" in data


def test_list_orders_empty():
    response = client.get("/orders")
    assert response.status_code == 200
    assert response.json() == []


def test_list_orders_after_create():
    client.post("/orders", json={"user_id": 1, "item": "Mouse", "quantity": 1})
    response = client.get("/orders")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_order_success():
    created = client.post("/orders", json={"user_id": 2, "item": "Keyboard", "quantity": 1}).json()
    response = client.get(f"/orders/{created['id']}")
    assert response.status_code == 200
    assert response.json()["item"] == "Keyboard"


def test_get_order_not_found():
    response = client.get("/orders/999")
    assert response.status_code == 404


def test_delete_order_success():
    created = client.post("/orders", json={"user_id": 3, "item": "Monitor", "quantity": 1}).json()
    response = client.delete(f"/orders/{created['id']}")
    assert response.status_code == 200
    # confirm it's actually gone
    get_response = client.get(f"/orders/{created['id']}")
    assert get_response.status_code == 404


def test_delete_order_not_found():
    response = client.delete("/orders/999")
    assert response.status_code == 404
