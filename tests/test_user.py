import pytest
from fastapi import status
from app.schemas import UserCreate, UserUpdate

def test_get_users_empty(client):
    response = client.get("/users/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

def test_get_users_with_data(client, test_user):
    response = client.get("/users/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["username"] == "testuser"

def test_get_user_by_id(client, test_user):
    response = client.get(f"/users/{test_user.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "testuser"

def test_get_nonexistent_user(client):
    response = client.get("/users/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"

def test_create_user(client):
    user_data = {
        "username": "newuser",
        "password": "newpass123",
        "first_name": "New",
        "last_name": "User"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["username"] == "newuser"
    assert "id" in data

def test_create_duplicate_user(client, test_user):
    user_data = {
        "username": "testuser",  
        "password": "testpass",
        "first_name": "Andrey"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Username already existed"

def test_update_user(client, test_user):
    update_data = {"first_name": "Updated"}
    response = client.put(f"/users/{test_user.id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["first_name"] == "Updated"

def test_update_nonexistent_user(client):
    response = client.put("/users/999", json={"first_name": "Updated"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"

def test_update_user(client, test_user):
    update_data = {"first_name": "Updated"}
    response = client.put(f"/users/{test_user.id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["first_name"] == "Updated"

def test_update_nonexistent_user(client):
    response = client.put("/users/999", json={"first_name": "Updated"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"

def test_delete_user(client, test_user):
    response = client.delete(f"/users/{test_user.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"user": "User deleted"}

    response = client.get(f"/users/{test_user.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_nonexistent_user(client):
    response = client.delete("/users/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"