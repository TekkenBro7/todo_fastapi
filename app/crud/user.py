from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.utils.security import get_password_hash
from app.schemas.user import UserCreate, UserUpdate
from app.models import User


async def read_user(
    db: AsyncSession,
    user_id: int
):
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()


async def read_users(
    db: AsyncSession,
    offset: int = 0,
    limit: int = 100
):
    result = await db.execute(select(User).offset(offset).limit(limit))
    return result.scalars().all()


async def read_user_by_username(
    db: AsyncSession,
    username: str
):
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalars().first()


async def create_user_db(
    db: AsyncSession, 
    user_data: UserCreate
):
    hashed_passowrd = get_password_hash(user_data.password)
    db_user = User(
        username=user_data.username,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        password=hashed_passowrd
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user_db(
    db: AsyncSession,
    user_id: int,
    user_data: UserUpdate
):
    db_user = await read_user(db, user_id)
    if not db_user:
        return None
    
    if user_data.username is not None and user_data.username != db_user.username:
        result = await db.execute(select(User).where(User.username == user_data.username, User.id != user_id))
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")
    
    for key, value in user_data.dict(exclude_none=True).items():
        print(value)
        setattr(db_user, key, value)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def delete_user_db(
    db: AsyncSession,
    user_id: int
):
    db_user = await read_user(db, user_id)
    if not db_user:
        return False
    await db.delete(db_user)
    await db.commit()
    return True