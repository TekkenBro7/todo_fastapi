#!/bin/sh
alembic upgrade head
uvicorn app.main:app --host 000.0.0.0 --port 8000