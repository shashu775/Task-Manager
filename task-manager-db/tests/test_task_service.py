import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'task-service'))

# Use SQLite in-memory for tests (no real Postgres needed)
os.environ["DATABASE_URL"] = "sqlite:///./test_tasks.db"

from fastapi.testclient import TestClient
from app.database import engine, Base
from app.main import app

Base.metadata.create_all(bind=engine)
client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["service"] == "task-service"

def test_create_task():
    r = client.post("/tasks", json={"title": "Learn CKA", "done": False})
    assert r.status_code == 201
    assert r.json()["title"] == "Learn CKA"
    assert "id" in r.json()

def test_list_tasks():
    r = client.get("/tasks")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_get_task():
    r = client.post("/tasks", json={"title": "Get Me"})
    task_id = r.json()["id"]
    r2 = client.get(f"/tasks/{task_id}")
    assert r2.status_code == 200
    assert r2.json()["id"] == task_id

def test_update_task():
    r = client.post("/tasks", json={"title": "Update Me", "done": False})
    task_id = r.json()["id"]
    r2 = client.patch(f"/tasks/{task_id}", json={"title": "Updated", "done": True})
    assert r2.status_code == 200
    assert r2.json()["done"] == True

def test_delete_task():
    r = client.post("/tasks", json={"title": "Delete Me"})
    task_id = r.json()["id"]
    client.delete(f"/tasks/{task_id}")
    r2 = client.get(f"/tasks/{task_id}")
    assert r2.status_code == 404

def test_task_not_found():
    r = client.get("/tasks/nonexistent-id")
    assert r.status_code == 404
