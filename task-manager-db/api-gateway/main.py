from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI(title="API Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

TASK_SERVICE = os.getenv("TASK_SERVICE_URL", "http://task-service:8001")
USER_SERVICE = os.getenv("USER_SERVICE_URL", "http://user-service:8002")

# ── Health ────────────────────────────────────────────────────────
@app.get("/health")
async def health():
    results = {}
    async with httpx.AsyncClient(timeout=3) as client:
        for name, url in [("task-service", TASK_SERVICE), ("user-service", USER_SERVICE)]:
            try:
                r = await client.get(f"{url}/health")
                results[name] = r.json()
            except Exception:
                results[name] = {"status": "unreachable"}
    return {"status": "ok", "service": "api-gateway", "upstream": results}

# ── Task routes ───────────────────────────────────────────────────
@app.get("/tasks")
async def get_tasks():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{TASK_SERVICE}/tasks")
        return r.json()

@app.post("/tasks")
async def create_task(request: Request):
    body = await request.json()
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{TASK_SERVICE}/tasks", json=body)
        if r.status_code >= 400:
            raise HTTPException(status_code=r.status_code, detail=r.json().get("detail"))
        return r.json()

@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{TASK_SERVICE}/tasks/{task_id}")
        if r.status_code == 404:
            raise HTTPException(status_code=404, detail="Task not found")
        return r.json()

@app.patch("/tasks/{task_id}")
async def update_task(task_id: str, request: Request):
    body = await request.json()
    async with httpx.AsyncClient() as client:
        r = await client.patch(f"{TASK_SERVICE}/tasks/{task_id}", json=body)
        if r.status_code == 404:
            raise HTTPException(status_code=404, detail="Task not found")
        return r.json()

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    async with httpx.AsyncClient() as client:
        r = await client.delete(f"{TASK_SERVICE}/tasks/{task_id}")
        if r.status_code == 404:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"deleted": task_id}

# ── User routes ───────────────────────────────────────────────────
@app.get("/users")
async def get_users():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{USER_SERVICE}/users")
        return r.json()

@app.post("/users")
async def create_user(request: Request):
    body = await request.json()
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{USER_SERVICE}/users", json=body)
        if r.status_code >= 400:
            raise HTTPException(status_code=r.status_code, detail=r.json().get("detail"))
        return r.json()

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{USER_SERVICE}/users/{user_id}")
        if r.status_code == 404:
            raise HTTPException(status_code=404, detail="User not found")
        return r.json()

@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    async with httpx.AsyncClient() as client:
        r = await client.delete(f"{USER_SERVICE}/users/{user_id}")
        if r.status_code == 404:
            raise HTTPException(status_code=404, detail="User not found")
        return {"deleted": user_id}
