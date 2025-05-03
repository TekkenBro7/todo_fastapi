from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Task, TaskStatus
from app.schemas import TaskCreate, TaskUpdate, TaskStatus


async def read_task(
    db: AsyncSession,
    task_id: int
):
    result = await db.execute(select(Task).filter(Task.id == task_id))
    return result.scalars().first()


async def read_tasks(
    db: AsyncSession, 
    skip: int = 0,
    limit: int = 100
):
    result = await db.execute(select(Task).offset(skip).limit(limit))
    return result.scalars().all()


async def read_user_tasks(
    db: AsyncSession,
    user_id: int,
    skip: int = 0, 
    limit: int = 100
):
    result = await db.execute(select(Task).filter(Task.user_id == user_id).offset(skip).limit(limit))
    return result.scalars().all()


async def create_task(
    db: AsyncSession, 
    task_data: TaskCreate,
    user_id: int
):
    task_dict = task_data.dict()
    db_task = Task(
        title=task_dict["title"],
        description=task_dict.get("description"),
        status=task_dict.get("status", "new"),
        user_id=user_id
    )
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def update_task(
    db: AsyncSession,
    task_id: int, 
    task_data: TaskUpdate,
    user_id: int
):
    task = await read_task(db, task_id)
    if not task or task.user_id != user_id:
        return None
    for key, value in task_data.dict(exclude_none=True).items():
        setattr(task, key, value)
    await db.commit()
    await db.refresh(task)
    return task


async def delete_task(
    db: AsyncSession,
    task_id: int,
    user_id: int
):
    task = await read_task(db, task_id)
    if not task or task.user_id != user_id:
        return False
    await db.delete(task)
    await db.commit()
    return True


async def mark_task_completed(
    db: AsyncSession,
    task_id: int, 
    user_id: int
):
    task = await read_task(db, task_id)
    if not task or task.user_id != user_id:
        return None
    task.status = TaskStatus.COMPLETED
    await db.commit()
    await db.refresh(task)
    return task


async def filter_by_status(
    db: AsyncSession,
    status: TaskStatus,
    skip: int = 0, 
    limit: int = 100
):
    result = await db.execute(select(Task).filter(Task.status == status).offset(skip).limit(limit))
    return result.scalars().all()