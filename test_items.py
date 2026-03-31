from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_all_items():
    response = client.get("/items/")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_single_item_success():
    response = client.get("/items/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_single_item_not_found():
    response = client.get("/items/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"