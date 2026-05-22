from pydantic import BaseModel
from datetime import datetime


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    source: str = "telegram"


class TaskUpdate(BaseModel):
    status: str


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: str
    source: str
    created_at: datetime

    class Config:
        from_attributes = True