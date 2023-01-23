from datetime import datetime
from typing import Union

from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    title: str
    description: Union[str, None] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Union[str, None] = Field(min_length=1)
    description: Union[str, None] = None


class TaskList:
    search_term: Union[str, None] = None


class TaskSchema(TaskBase):
    id: int
    completed: bool
    deleted: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: Union[datetime, None] = None

    class Config:
        orm_mode = True
