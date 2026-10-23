from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.task import Task
from app.models.checklist import Checklist
from app.models.user import User
from app.api.deps import get_current_user

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/")
def get_dashboard_metrics(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_tasks = db.query(Task).join(Checklist).filter(Checklist.userId == current_user.id, Task.deletedAt == None)
    
    total = user_tasks.count()
    completed = user_tasks.filter(Task.status == "DONE").count()
    pending = user_tasks.filter(Task.status == "PENDING").count()
    late = user_tasks.filter(Task.status == "LATE").count()
    
    return {
        "total_tasks": total,
        "completed_tasks": completed,
        "pending_tasks": pending,
        "late_tasks": late
    }
