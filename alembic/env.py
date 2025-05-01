from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import create_async_engine
import asyncio

from alembic import context
import sys
from os.path import abspath, dirname

# Добавляем путь к проекту в PYTHONPATH
sys.path.insert(0, dirname(dirname(abspath(__file__))))

from app.database import Base
from app.models.user import User
from app.models.task import Task
from app.config import settings

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=settings.DB_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(
        connection=connection, 
        target_metadata=target_metadata,
        compare_type=True,
        render_as_batch=True
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations():
    """Run migrations in 'online' mode with async engine."""
    connectable = create_async_engine(settings.DB_URL)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    
    await connectable.dispose()

if context.is_offline_mode():
    print(2)
    run_migrations_offline()
else:
    print(3)
    asyncio.run(run_async_migrations())