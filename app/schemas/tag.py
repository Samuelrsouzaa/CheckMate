from pydantic import BaseModel
from datetime import datetime

class TagBase(BaseModel):
    name: str
    color: str

class TagCreate(TagBase):
    pass

class TagOut(TagBase):
    id: int
    userId: int
    createdAt: datetime

    class Config:
        from_attributes = True
