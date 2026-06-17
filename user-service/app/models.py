from sqlalchemy import Column, String
from app.database import Base
from pydantic import BaseModel
import uuid

# ── SQLAlchemy ORM model ──────────────────────────────────────────
class UserORM(Base):
    __tablename__ = "users"

    id    = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name  = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)

# ── Pydantic schemas ──────────────────────────────────────────────
class UserCreate(BaseModel):
    name:  str
    email: str

class User(BaseModel):
    id:    str
    name:  str
    email: str

    class Config:
        from_attributes = True
