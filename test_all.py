from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# =====================
# AUTH
# =====================
def test_login_success():
    res = client.post("/login", json={"username": "admin", "password": "admin123"})
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_login_fail():
    res = client.post("/login", json={"username": "admin", "password": "wrong"})
    assert res.status_code == 401


# =====================
# CRUD
# =====================
def test_create_item():
    res = client.post("/items/", json={"name": "Test", "description": "Desc"})
    assert res.status_code == 200


def test_get_items():
    res = client.get("/items/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_update_item():
    create = client.post("/items/", json={"name": "Old", "description": "Old"})
    item_id = create.json()["id"]

    res = client.put(f"/items/{item_id}", json={"name": "New", "description": "New"})
    assert res.status_code == 200
    assert res.json()["name"] == "New"


def test_delete_admin():
    create = client.post("/items/", json={"name": "Delete", "description": "Test"})
    item_id = create.json()["id"]

    res = client.delete(f"/items/{item_id}?token=admin")
    assert res.status_code == 200


# =====================
# RBAC
# =====================
def test_delete_user_forbidden():
    create = client.post("/items/", json={"name": "Protected", "description": "Test"})
    item_id = create.json()["id"]

    res = client.delete(f"/items/{item_id}?token=user")
    assert res.status_code == 403