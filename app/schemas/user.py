from pydantic import BaseModel, Field, constr
from typing import Optional, Annotated

NonEmptyStr = Annotated[str, Field(min_length=1, strip_whitespace=True)]

class UserBase(BaseModel):
    first_name : str
    last_name : Optional[str] = None
    username: str


class UserCreate(UserBase):
    password : str = Field(min_length=4)


class UserUpdate(BaseModel):
    first_name: Optional[NonEmptyStr] = None
    last_name: Optional[NonEmptyStr] = None
    username: Optional[NonEmptyStr] = None


class UserOut(UserBase):
    id : int
    
    class Config:
        from_attributes = True # to serialize SQLAlchemy object to JSON