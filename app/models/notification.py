from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    taskId = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=True)
    type = Column(String(50), nullable=False) # REMINDER, OVERDUE, SYSTEM
    channel = Column(String(20), default="EMAIL") # EMAIL, PUSH, BOTH
    scheduledAt = Column(DateTime(timezone=True), nullable=False)
    sentAt = Column(DateTime(timezone=True), nullable=True)
    isRead = Column(Boolean, default=False)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="notifications")
    task = relationship("Task", back_populates="notifications")
