from typing import Optional
import uuid
from pydantic import BaseModel, Field


class User(BaseModel):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4)
    name: str
    email: str
    password: str


class Task(BaseModel):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4)
    title: str
    description: str
    completed: bool = False
    user_id: uuid.UUID
