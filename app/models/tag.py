from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(50), nullable=False)
    color = Column(String(7), nullable=False) # hex
    createdAt = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="tags")
    tasks = relationship("Task", secondary="task_tags", back_populates="tags")
