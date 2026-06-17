import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'user-service'))

os.environ["DATABASE_URL"] = "sqlite:///./test_users.db"

from fastapi.testclient import TestClient
from app.database import engine, Base
from app.main import app

Base.metadata.create_all(bind=engine)
client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["service"] == "user-service"

def test_create_user():
    r = client.post("/users", json={"name": "Shashwat", "email": "shashu@unique1.com"})
    assert r.status_code == 201
    assert r.json()["name"] == "Shashwat"

def test_list_users():
    r = client.get("/users")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_get_user():
    r = client.post("/users", json={"name": "Test User", "email": "test@unique2.com"})
    user_id = r.json()["id"]
    r2 = client.get(f"/users/{user_id}")
    assert r2.status_code == 200

def test_duplicate_email():
    client.post("/users", json={"name": "First", "email": "dup@unique3.com"})
    r2 = client.post("/users", json={"name": "Second", "email": "dup@unique3.com"})
    assert r2.status_code == 409

def test_delete_user():
    r = client.post("/users", json={"name": "Delete Me", "email": "del@unique4.com"})
    user_id = r.json()["id"]
    client.delete(f"/users/{user_id}")
    assert client.get(f"/users/{user_id}").status_code == 404
