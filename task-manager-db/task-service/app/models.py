from sqlalchemy import Column, String, Boolean
from app.database import Base
from pydantic import BaseModel
import uuid

# ── SQLAlchemy ORM model (maps to DB table) ──────────────────────
class TaskORM(Base):
    __tablename__ = "tasks"

    id      = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title   = Column(String, nullable=False)
    done    = Column(Boolean, default=False)
    user_id = Column(String, default="")

# ── Pydantic schemas (request/response validation) ────────────────
class TaskCreate(BaseModel):
    title:   str
    done:    bool = False
    user_id: str  = ""

class TaskUpdate(BaseModel):
    title:   str
    done:    bool
    user_id: str = ""

class Task(BaseModel):
    id:      str
    title:   str
    done:    bool
    user_id: str

    class Config:
        from_attributes = True
