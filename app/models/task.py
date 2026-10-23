from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base

task_tags = Table(
    "task_tags",
    Base.metadata,
    Column("taskId", Integer, ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True),
    Column("tagId", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    checklistId = Column(Integer, ForeignKey("checklists.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    dueDate = Column(DateTime(timezone=True), nullable=True)
    priority = Column(String(10), default="MED") # HIGH, MED, LOW
    status = Column(String(20), default="PENDING") # PENDING, DONE, LATE
    position = Column(Integer, default=0)
    completedAt = Column(DateTime(timezone=True), nullable=True)
    deletedAt = Column(DateTime(timezone=True), nullable=True) # Soft delete
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now())

    checklist = relationship("Checklist", back_populates="tasks")
    tags = relationship("Tag", secondary=task_tags, back_populates="tasks")
    notifications = relationship("Notification", back_populates="task", cascade="all, delete-orphan")
