from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import task

router = APIRouter()

@router.get("/tasks/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    db_task = task.read_tasks(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task