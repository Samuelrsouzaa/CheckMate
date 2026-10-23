from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ChecklistBase(BaseModel):
    name: str
    description: Optional[str] = None

class ChecklistCreate(ChecklistBase):
    pass

class ChecklistUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    isArchived: Optional[bool] = None

class ChecklistOut(ChecklistBase):
    id: int
    userId: int
    isArchived: bool
    createdAt: datetime
    updatedAt: Optional[datetime] = None

    class Config:
        from_attributes = True
