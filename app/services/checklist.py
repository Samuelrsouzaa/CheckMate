from sqlalchemy.orm import Session
from app.models.checklist import Checklist
from app.schemas.checklist import ChecklistCreate, ChecklistUpdate
from fastapi import HTTPException

def get_checklists(db: Session, user_id: int):
    return db.query(Checklist).filter(Checklist.userId == user_id).all()

def get_checklist(db: Session, checklist_id: int, user_id: int):
    return db.query(Checklist).filter(Checklist.id == checklist_id, Checklist.userId == user_id).first()

def create_checklist(db: Session, checklist: ChecklistCreate, user_id: int):
    # Rule RN01 limit 50 checklists for free account
    count = db.query(Checklist).filter(Checklist.userId == user_id, Checklist.isArchived == False).count()
    if count >= 50:
        raise HTTPException(status_code=403, detail="Free accounts are limited to 50 active checklists.")
        
    db_checklist = Checklist(**checklist.model_dump(), userId=user_id)
    db.add(db_checklist)
    db.commit()
    db.refresh(db_checklist)
    return db_checklist

def update_checklist(db: Session, checklist_id: int, user_id: int, checklist: ChecklistUpdate):
    db_checklist = get_checklist(db, checklist_id, user_id)
    if not db_checklist:
        return None
    for var, value in vars(checklist).items():
        if value is not None:
            setattr(db_checklist, var, value)
    db.commit()
    db.refresh(db_checklist)
    return db_checklist

def delete_checklist(db: Session, checklist_id: int, user_id: int):
    db_checklist = get_checklist(db, checklist_id, user_id)
    if not db_checklist:
        return None
    # RN04: Cannot delete if tasks are "PENDING" (ignorando as que já foram para a lixeira)
    pending_tasks = any(task.status == "PENDING" and task.deletedAt is None for task in db_checklist.tasks)
    if pending_tasks:
        raise HTTPException(status_code=400, detail="Cannot delete checklist with pending tasks.")
        
    db.delete(db_checklist)
    db.commit()
    return db_checklist
