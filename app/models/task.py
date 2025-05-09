from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey
from app.utils.timestamp_mixin import TimestampMixin
from sqlalchemy.orm import relationship
import enum

from ..database import Base


class TaskStatus(enum.Enum):
    NEW = "New"
    IN_PROGRESS = "In_Progress"
    COMPLETED = "Completed"


class Task(Base, TimestampMixin):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  
    title = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.NEW)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    owner = relationship("User", back_populates="tasks")    