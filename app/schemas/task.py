from pydantic import BaseModel, Field
from typing import Optional

from app.models.task import TaskStatus
from app.schemas.user import NonEmptyStr 


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: TaskStatus = TaskStatus.NEW


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    title: Optional[NonEmptyStr] = None
    description: Optional[NonEmptyStr] = None


class TaskOut(TaskBase):
    id : int
    user_id : int
    
    class Config:
        from_attributes = True # to serialize SQLAlchemy object to JSON