from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut
from app.services import task as task_service
from app.models.user import User
from app.api.deps import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/checklist/{checklist_id}", response_model=List[TaskOut])
def read_tasks(checklist_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return task_service.get_tasks_by_checklist(db=db, checklist_id=checklist_id, user_id=current_user.id)

@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not task_in.title or len(task_in.title) < 3:
        raise HTTPException(status_code=422, detail="Título é obrigatório e deve ter no mínimo 3 caracteres.")
    return task_service.create_task(db=db, task=task_in, user_id=current_user.id)

@router.put("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task_in: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = task_service.update_task(db=db, task_id=task_id, user_id=current_user.id, task_update=task_in)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/{task_id}", response_model=TaskOut)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = task_service.delete_task(db=db, task_id=task_id, user_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
