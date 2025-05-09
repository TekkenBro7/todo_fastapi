from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import declared_attr
from datetime import datetime


class TimestampMixin:
    @declared_attr
    def created_at(cls):
        return Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    @declared_attr
    def updated_at(cls):
        return Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now(), nullable=False)