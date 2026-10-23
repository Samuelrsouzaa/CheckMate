from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .tag import TagOut

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    dueDate: Optional[datetime] = None
    priority: Optional[str] = "MED" # HIGH, MED, LOW

class TaskCreate(TaskBase):
    checklistId: int

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    dueDate: Optional[datetime] = None
    priority: Optional[str] = None
    status: Optional[str] = None # PENDING, DONE, LATE
    position: Optional[int] = None

class TaskOut(TaskBase):
    id: int
    checklistId: int
    status: str
    position: int
    completedAt: Optional[datetime] = None
    deletedAt: Optional[datetime] = None
    createdAt: datetime
    updatedAt: Optional[datetime] = None
    tags: List[TagOut] = []

    class Config:
        from_attributes = True
