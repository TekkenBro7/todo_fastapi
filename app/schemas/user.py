from pydantic import BaseModel, Field
from typing import Optional


class UserBase(BaseModel):
    first_name : str
    last_name : Optional[str] = None
    username: str


class UserCreate(UserBase):
    password : str = Field(min_length=4)