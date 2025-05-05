# 🚀 FastAPI PostgreSQL Alembic Application

A production-ready FastAPI application using PostgreSQL, Docker, and Alembic for migrations. Easily configurable with environment variables and fully containerized for development and deployment.

---

## 📁 Project Structure

```text
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── models               # SQLAlchemy models
│   ├── schemas              # Pydantic schemas
│   ├── database.py          # Database connection
|   ├── crud                 # Working with database
|   ├── routes               # Endpoints of API
│   └── ...
├── alembic/
│   └── versions/            # Alembic migration scripts
├── alembic.ini              # Alembic configuration
├── tests/
│   └── test_*.py            # Unit tests
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker image for app
├── docker-compose.yml       # Service definitions
├── .env                     # Environment variables
├── .dockerignore
└── README.md
```

## ⚡ Quick Start

```bash
# 1. Clone repository
git clone https://github.com/TekkenBro7/todo_fastapi.git
cd todo_fastapi

# 2. (Optional) Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# 3. Install dependencies
pip install -r requirements.txt

```

Example of **.env** file:
```bash
# Database Configuration
POSTGRES_USER=""
POSTGRES_PASSWORD=""
POSTGRES_DB=""
DATABASE_URL=""  # example "postgresql+asyncpg://POSTGRES_USER:POSTGRES_PASSWORD@localhost:5432/POSTGRES_DB"
DOCKER_DATABASE_URL=""  # for docker, example "postgresql+asyncpg://POSTGRES_USER:POSTGRES_PASSWORD@db:5432/POSTGRES_DB"

# Application Settings
SECRET_KEY="your-secret-key-here"  # For JWT tokens
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES="30"
DEBUG="True"
```

## 🛠️ Alembic Migrations
Once your database is configured and the **.env** file is ready, you need to apply migrations using Alembic to create the necessary tables and schema.

### 📌 Creating a New Migration
To generate a new migration after updating or adding models:
```bash
# If using Docker
docker-compose exec app alembic revision --autogenerate -m "your message here"

# Or locally (if not using Docker)
alembic revision --autogenerate -m "your message here"
```
This will create a new file in the alembic/versions/ directory containing the migration script.

### ✅ Applying Migrations
To apply the latest migration to your database:

```bash
# If using Docker (not necessarily as with a file start.sh it makes itself)
docker-compose exec app alembic upgrade head

# Or locally
alembic upgrade head
```
This ensures your database schema is up to date with the current models.

## 🚀 Running the App

### 🔧 Using Uvicorn (Locally)
```bash
# Make sure the virtual environment is activated and dependencies installed

# Apply Alembic migrations (if not done yet)
alembic upgrade head

# Run FastAPI app using Uvicorn
uvicorn app.main:app --reload
```

### 🐳 Using Docker
```bash
# Build and start containers
docker-compose up --build
```
This starts the FastAPI app and PostgreSQL database. Default URL: http://localhost:8000

To stop and remove containers:
```bash
docker-compose down
```

## 📌 API Authentication (JWT)
This application uses JWT (JSON Web Tokens) for authentication.

### 🛠 Generating a Token
Send a POST request to **/auth/login** with valid credentials:

```json
POST /auth/login
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```
Response:
```json
{
  "access_token": "your.jwt.token",
  "token_type": "bearer"
}
```
Include this token in the **Authorization** header when making authorized requests:
```json
Authorization: Bearer your.jwt.token
```

## 🧪 Running Tests
All tests have been tested on endpoints (auth, task, user). To run the tests, write to the command line.

```bash
# Run all tests
pytest

# Run specific test module
pytest tests/test_tasks.py
```
