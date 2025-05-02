from .user import router as user_router
from .task import router as task_router
from fastapi import APIRouter 

main_route = APIRouter()

main_route.include_router(user_router)