# 🚀 FastAPI PostgreSQL Docker Application

A production-ready FastAPI application using PostgreSQL, Docker, and Alembic for migrations. Easily configurable with environment variables and fully containerized for development and deployment.

---

## 📁 Project Structure

```text
.
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
cd todo-fastapi

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
