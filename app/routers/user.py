from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import user
from app.schemas import UserOut, UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get('/', response_model=list[UserOut])
async def get_users(db: AsyncSession = Depends(get_db), limit: int = 100, offset: int = 0):
    return await user.read_users(db, limit=limit, offset=offset)


@router.get('/{user_id}', response_model=UserOut)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await user.read_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post('/', response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(userScheme: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await user.read_user_by_username(db, userScheme.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already existed")
    return await user.create_user_db(db, userScheme)


@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user_data: UserUpdate, db: AsyncSession = Depends(get_db)):
    db_user = await user.update_user_db(db, user_id, user_data)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    success = await user.delete_user_db(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")