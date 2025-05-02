from pydantic import BaseModel, Field
from typing import Optional
from app.models.task import TaskStatus


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.NEW


class TaskCreate(BaseModel):
    pass


class TaskOut(TaskBase):
    id : int
    
    class Config:
        orm_mode = True # to serialize SQLAlchemy object to JSON