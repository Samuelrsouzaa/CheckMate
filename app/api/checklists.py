from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.checklist import ChecklistCreate, ChecklistUpdate, ChecklistOut
from app.services import checklist as checklist_service
from app.models.user import User
from app.api.deps import get_current_user

router = APIRouter(prefix="/checklists", tags=["checklists"])

@router.get("/", response_model=List[ChecklistOut])
def read_checklists(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return checklist_service.get_checklists(db=db, user_id=current_user.id)

@router.post("/", response_model=ChecklistOut, status_code=status.HTTP_201_CREATED)
def create_checklist(checklist_in: ChecklistCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return checklist_service.create_checklist(db=db, checklist=checklist_in, user_id=current_user.id)

@router.put("/{checklist_id}", response_model=ChecklistOut)
def update_checklist(checklist_id: int, checklist_in: ChecklistUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    checklist = checklist_service.update_checklist(db=db, checklist_id=checklist_id, user_id=current_user.id, checklist=checklist_in)
    if not checklist:
        raise HTTPException(status_code=404, detail="Checklist not found")
    return checklist

@router.delete("/{checklist_id}", response_model=ChecklistOut)
def delete_checklist(checklist_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    checklist = checklist_service.delete_checklist(db=db, checklist_id=checklist_id, user_id=current_user.id)
    if not checklist:
        raise HTTPException(status_code=404, detail="Checklist not found")
    return checklist
