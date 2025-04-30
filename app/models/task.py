from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from ..database import Base
import enum


class TaskStatus():
    NEW = "New"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"