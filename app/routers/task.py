from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.database import get_db
from app.schemas import TaskOut, TaskCreate, TaskUpdate, TaskStatus
from app.crud import task
from app.utils.security import get_current_user, get_current_user_id
from app.models import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=List[TaskOut])
async def get_tasks(
    skip: int = 0,
    limit: int = 100,
    status: Optional[TaskStatus] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if status:
        return await task.filter_by_status(db, status, skip, limit)
    return await task.read_tasks(db, skip, limit)


@router.get("/my", response_model=List[TaskOut])
async def get_user_tasks(
    skip: int = 0,
    limit: int = 100,
    status: Optional[TaskStatus] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if status:
        tasks = await task.read_user_tasks(db, current_user.id, skip, limit)
        return [task for task in tasks if task.status == status]
    return await task.read_user_tasks(db, current_user.id, skip, limit)


@router.get("/filter/{status}", response_model=List[TaskOut])
async def filter_tasks_by_status(
    status: TaskStatus,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    return await task.filter_by_status(db, status, skip, limit)


@router.get("/{task_id}", response_model=TaskOut)
async def get_task(
    task_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_db = await task.read_task(db, task_id)
    if not task_db:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_db


@router.post("/", response_model=TaskOut)
async def create_task(
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db), 
    current_user_id: int = Depends(get_current_user_id),
):
    try:
        created_task = await task.create_task(db, task_data, current_user_id)
        return created_task
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating task: {str(e)}"
        )


@router.put("/{task_id}", response_model=TaskOut)
async def update_task(task_id: int, 
    task_data: TaskUpdate, 
    db: AsyncSession = Depends(get_db), 
    current_user_id: int = Depends(get_current_user_id)
):
    task_db = await task.update_task(db, task_id, task_data, current_user_id)
    if not task_db:
        raise HTTPException(status_code=403, detail="Forbidden or task not found")
    return task_db


@router.delete("/{task_id}")
async def delete_task(
    task_id: int, 
    db: AsyncSession = Depends(get_db), 
    user_id: int = Depends(get_current_user_id)
):
    success = await task.delete_task(db, task_id, user_id)
    if not success:
        raise HTTPException(status_code=403, detail="Forbidden or task not found")
    return {"detail": "Task deleted"}


@router.post("/{task_id}/complete", response_model=TaskOut)
async def complete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db), 
    user_id: int = Depends(get_current_user_id)
):
    task_db = await task.mark_task_completed(db, task_id, user_id)
    if not task_db:
        raise HTTPException(status_code=403, detail="Forbidden or task not found")
    return task_db