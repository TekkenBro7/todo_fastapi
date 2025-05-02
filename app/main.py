from fastapi import FastAPI
import uvicorn
from .database import engine, Base
from .models import user, task
from app.routers import main_route
from app.config import settings

app = FastAPI(title=settings.TITLE)

app.include_router(main_route)

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI"}


# @app.on_event("startup")
# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)