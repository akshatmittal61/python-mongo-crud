from typing import Optional
import uuid
from pydantic import BaseModel, Field


class Task(BaseModel):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4)
    title: str
    description: str
    completed: bool = False

    def create_task(self, title: str, description: str):
        self.title = title
        self.description = description

    def toggle_completion(self):
        self.completed = False if self.completed else True
