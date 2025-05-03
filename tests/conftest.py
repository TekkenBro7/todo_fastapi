import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db, Base
from app.models import User
from app.utils.security import get_password_hash
from app.models.task import TaskStatus

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="function")
def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    
    with TestClient(app) as client:
        yield client
    
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
async def async_engine():
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    yield engine
    await engine.dispose()

@pytest.fixture(scope="function")
async def setup_db(async_engine):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def db_session(async_engine, setup_db):
    async_session = sessionmaker(
        async_engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        yield session

@pytest.fixture
async def test_user(db_session):
    user = User(
        username="testuser",
        password=get_password_hash("testpass"),
        first_name="Maxim",
        last_name="Sniazhko"
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest.fixture
def auth_headers(client, test_user):
    login_res = client.post("/auth/login", data={
        "username": "testuser", 
        "password": "testpass"
    })
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def test_task(client, auth_headers):
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "status": TaskStatus.IN_PROGRESS.value
    }
    response = client.post(
        "/tasks/",
        json=task_data,
        headers=auth_headers
    )
    return response.json()