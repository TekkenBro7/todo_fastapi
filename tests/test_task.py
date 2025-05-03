import pytest
from fastapi import status
from app.schemas import TaskStatus, TaskCreate, TaskUpdate

def test_create_task(client, test_user):
    login_data = {
        "username": "testuser",
        "password": "testpass"
    }
    login_response = client.post("/auth/login", data=login_data)
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "status": TaskStatus.IN_PROGRESS.value
    }
    response = client.post(
        "/tasks/",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    result = response.json()
    assert result["title"] == "Test Task"
    assert result["status"] == TaskStatus.IN_PROGRESS.value
    assert result["user_id"] == test_user.id

def test_get_all_tasks(client, test_task, auth_headers):
    response = client.get(
        "/tasks/",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    tasks = response.json()
    
    assert len(tasks) >= 1
    assert any(t["id"] == test_task["id"] for t in tasks)
    assert any(t["title"] == "Test Task" for t in tasks)

def test_get_tasks_filtered_by_status(client, auth_headers):
    task_data = {
        "title": "Pending Task",
        "status": TaskStatus.COMPLETED.value
    }
    client.post("/tasks/", json=task_data, headers=auth_headers)
    
    response = client.get(
        f"/tasks/?status={TaskStatus.COMPLETED.value}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    tasks = response.json()
    assert all(t["status"] == TaskStatus.COMPLETED.value for t in tasks)

def test_get_user_tasks(client, test_task, auth_headers):
    response = client.get("/tasks/my", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == test_task["id"]

def test_get_user_tasks_filtered(client, auth_headers):
    task_data = [
        {"title": "Task 1", "status": TaskStatus.IN_PROGRESS.value},
        {"title": "Task 2", "status": TaskStatus.COMPLETED.value}
    ]
    for data in task_data:
        client.post("/tasks/", json=data, headers=auth_headers)
    
    response = client.get(
        f"/tasks/my?status={TaskStatus.IN_PROGRESS.value}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    tasks = response.json()
    assert all(t["status"] == TaskStatus.IN_PROGRESS.value for t in tasks)

def test_get_task_by_id(client, test_task, auth_headers):
    response = client.get(
        f"/tasks/{test_task['id']}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Test Task"

def test_get_nonexistent_task(client, auth_headers):
    response = client.get("/tasks/999999", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_create_task(client, auth_headers):
    task_data = {
        "title": "New Task",
        "status": TaskStatus.NEW.value
    }
    response = client.post(
        "/tasks/",
        json=task_data,
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "New Task"

def test_create_task_invalid_data(client, auth_headers):
    response = client.post(
        "/tasks/",
        json={"title": ""},
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_update_task(client, test_task, auth_headers):
    update_data = {
        "title": "Updated Task",
        "status": TaskStatus.COMPLETED.value
    }
    response = client.put(
        f"/tasks/{test_task['id']}",
        json=update_data,
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Updated Task"
    assert response.json()["status"] == TaskStatus.COMPLETED.value

def test_update_nonexistent_task(client, auth_headers):
    response = client.put(
        "/tasks/999999",
        json={"title": "Updated"},
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_delete_task(client, test_task, auth_headers):
    response = client.get(
        f"/tasks/{test_task['id']}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    
    response = client.delete(
        f"/tasks/{test_task['id']}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    
    response = client.get(
        f"/tasks/{test_task['id']}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_complete_task(client, test_task, auth_headers):
    response = client.post(
        f"/tasks/{test_task['id']}/complete",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == TaskStatus.COMPLETED.value

def test_complete_already_completed_task(client, auth_headers):
    task_data = {
        "title": "Completed Task",
        "status": TaskStatus.COMPLETED.value
    }
    response = client.post(
        "/tasks/",
        json=task_data,
        headers=auth_headers
    )
    task_id = response.json()["id"]
    
    response = client.post(
        f"/tasks/{task_id}/complete",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK

def test_get_tasks_pagination(client, auth_headers):
    for i in range(1, 16):
        task_data = {
            "title": f"Task {i}",
            "status": TaskStatus.NEW.value if i % 2 else TaskStatus.IN_PROGRESS.value
        }
        client.post("/tasks/", json=task_data, headers=auth_headers)
    
    response = client.get("/tasks/?limit=5", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5
    
    first_page = client.get("/tasks/?limit=5&skip=0", headers=auth_headers).json()
    second_page = client.get("/tasks/?limit=5&skip=5", headers=auth_headers).json()
    assert first_page[0]["title"] != second_page[0]["title"]
    
    response = client.get("/tasks/?limit=3&skip=10", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 3
    assert response.json()[0]["title"] == "Task 11"

def test_get_tasks_filter_by_status(client, auth_headers):
    statuses = [TaskStatus.NEW, TaskStatus.IN_PROGRESS, TaskStatus.COMPLETED]
    for i, status_task in enumerate(statuses, 1):
        task_data = {
            "title": f"Task {i}",
            "status": status_task.value
        }
        client.post("/tasks/", json=task_data, headers=auth_headers)
    
    for status_task in statuses:
        response = client.get(f"/tasks/?status={status_task.value}", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        tasks = response.json()
        assert all(t["status"] == status_task.value for t in tasks)
    
    response = client.get(
        f"/tasks/?status={TaskStatus.NEW.value}&limit=1&skip=0",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0]["status"] == TaskStatus.NEW.value

def test_get_tasks_empty_db(client, auth_headers):
    response = client.get("/tasks/", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
    
    response = client.get(
        f"/tasks/?status={TaskStatus.NEW.value}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

def test_get_tasks_invalid_status(client, auth_headers):
    response = client.get("/tasks/?status=invalid", headers=auth_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY