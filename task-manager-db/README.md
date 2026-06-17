# Task Manager — Microservices + PostgreSQL

## Architecture

```
Client (Browser)
      │
      ▼
 Frontend (nginx :3000)
      │
      ▼
 API Gateway (:8000)
      │
      ├──► Task Service (:8001) ──► PostgreSQL task-db (:5432)
      │
      └──► User Service (:8002) ──► PostgreSQL user-db (:5433)
```

## Quick Start — Docker Compose

```bash
docker-compose up --build
```

| Service      | URL                        |
|-------------|----------------------------|
| Frontend     | http://localhost:3000       |
| API Gateway  | http://localhost:8000       |
| API Docs     | http://localhost:8000/docs  |
| Task DB      | localhost:5432              |
| User DB      | localhost:5433              |

## Run Without Docker (3 terminals)

```bash
# Start PostgreSQL first (Docker)
docker run -d --name task-db -e POSTGRES_USER=taskuser \
  -e POSTGRES_PASSWORD=taskpass -e POSTGRES_DB=taskdb -p 5432:5432 postgres:15-alpine

docker run -d --name user-db -e POSTGRES_USER=useruser \
  -e POSTGRES_PASSWORD=userpass -e POSTGRES_DB=userdb -p 5433:5432 postgres:15-alpine

# Terminal 1 — Task Service
cd task-service && pip install -r requirements.txt
DATABASE_URL=postgresql://taskuser:taskpass@localhost:5432/taskdb \
  uvicorn app.main:app --host 0.0.0.0 --port 8001

# Terminal 2 — User Service
cd user-service && pip install -r requirements.txt
DATABASE_URL=postgresql://useruser:userpass@localhost:5433/userdb \
  uvicorn app.main:app --host 0.0.0.0 --port 8002

# Terminal 3 — API Gateway
cd api-gateway && pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Run Tests

```bash
pip install pytest httpx sqlalchemy
pytest tests/ -v
```

## Deploy to Kubernetes

```bash
# 1. Replace <DOCKERHUB_USER> in k8s/manifests.yaml
# 2. Apply
kubectl apply -f k8s/manifests.yaml
kubectl get pods -n task-manager

# Access
# Frontend:    http://<node-ip>:30090
# API Gateway: http://<node-ip>:30080
```

## What Changed vs In-Memory Version

| Layer        | Before         | Now                      |
|--------------|----------------|--------------------------|
| Storage      | Python dict    | PostgreSQL               |
| ORM          | None           | SQLAlchemy               |
| Models       | Pydantic only  | SQLAlchemy ORM + Pydantic|
| Persistence  | Lost on restart| Survives restarts        |
| K8s DB       | None           | StatefulSet + PVC        |
| Validation   | Basic          | Duplicate email check    |

## GitHub Secrets Required
- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`
