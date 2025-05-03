import pytest
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import User

def test_login_success(client, test_user):
    login_data = {
        "username": "testuser",
        "password": "testpass"
    }
    response = client.post("/auth/login", data=login_data)
    
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_wrong_password(client, test_user):
    login_data = {
        "username": "testuser",
        "password": "wrongpassword"
    }
    response = client.post("/auth/login", data=login_data)
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Incorrect username or password"

def test_login_nonexistent_user(client):
    login_data = {
        "username": "nonexistent",
        "password": "whatever"
    }
    response = client.post("/auth/login", data=login_data)
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Incorrect username or password"

async def test_login_verify_token(client, test_user, db_session: AsyncSession):
    login_data = {
        "username": "testuser",
        "password": "testpass"
    }
    login_response = client.post("/auth/login", data=login_data)
    token = login_response.json()["access_token"]
    
    tasks_response = client.get(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert tasks_response.status_code == status.HTTP_200_OK
