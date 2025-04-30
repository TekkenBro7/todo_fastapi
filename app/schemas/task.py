from pydantic import BaseModel, Field
from typing import Optional
from app.models.task import TaskStatus


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status = TaskStatus.NEW


class TaskCreate(BaseModel):
    pass