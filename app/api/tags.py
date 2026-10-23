from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.tag import TagCreate, TagOut
from app.models.tag import Tag
from app.models.user import User
from app.api.deps import get_current_user

router = APIRouter(prefix="/tags", tags=["tags"])

@router.get("/", response_model=List[TagOut])
def read_tags(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Tag).filter(Tag.userId == current_user.id).all()

@router.post("/", response_model=TagOut)
def create_tag(tag_in: TagCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_tag = Tag(**tag_in.model_dump(), userId=current_user.id)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag
