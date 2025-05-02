from sqlalchemy.orm import Session
from app.models import Task


def read_tasks(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()