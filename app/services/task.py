from sqlalchemy.orm import Session
from app.models.task import Task
from app.models.checklist import Checklist
from app.schemas.task import TaskCreate, TaskUpdate
from fastapi import HTTPException
from datetime import datetime

def get_tasks_by_checklist(db: Session, checklist_id: int, user_id: int):
    # Verify owner
    checklist = db.query(Checklist).filter(Checklist.id == checklist_id, Checklist.userId == user_id).first()
    if not checklist:
        raise HTTPException(status_code=404, detail="Checklist not found")
    return db.query(Task).filter(Task.checklistId == checklist_id, Task.deletedAt == None).all()

def create_task(db: Session, task: TaskCreate, user_id: int):
    # Verify checklist owner
    checklist = db.query(Checklist).filter(Checklist.id == task.checklistId, Checklist.userId == user_id).first()
    if not checklist:
        raise HTTPException(status_code=404, detail="Checklist not found")
    
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, user_id: int, task_update: TaskUpdate):
    db_task = db.query(Task).join(Checklist).filter(Task.id == task_id, Checklist.userId == user_id).first()
    if not db_task:
        return None
        
    for var, value in vars(task_update).items():
        if value is not None:
            setattr(db_task, var, value)
            if var == 'status' and value == 'DONE':
                db_task.completedAt = datetime.utcnow()
                
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int, user_id: int):
    db_task = db.query(Task).join(Checklist).filter(Task.id == task_id, Checklist.userId == user_id).first()
    if not db_task:
        return None
    # Soft delete (Lixeira)
    db_task.deletedAt = datetime.utcnow()
    db.commit()
    return db_task
