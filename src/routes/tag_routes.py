from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Tuple

from utils.session import get_db
from models.tag_models import Tag
from schemas.tag_schemas import TagSchema, TagCreate, TagUpdate
from schemas.pagination_schemas import PaginatedResponse
from utils.pagination import pagination_params

router = APIRouter(prefix="/tags", tags=["Tags"])

@router.get("/", response_model=PaginatedResponse[TagSchema])
def get_all_tags(pagination: Tuple[int, int] = Depends(pagination_params), db: Session = Depends(get_db)):
    skip, limit = pagination
    total = db.query(Tag).count()
    items = db.query(Tag).offset(skip).limit(limit).all()
    return PaginatedResponse(total=total, skip=skip, limit=limit, items=items)

@router.get("/{id}", response_model=TagSchema)
def get_tag_by_id(id: int, db: Session = Depends(get_db)):
    tag = db.query(Tag).filter(Tag.id == id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

@router.post("/", response_model=TagSchema)
def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    new_tag = Tag(**tag.model_dump())
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return new_tag

@router.put("/{id}", response_model=TagSchema)
def update_tag(id: int, tag: TagUpdate, db: Session = Depends(get_db)):
    db_tag = db.query(Tag).filter(Tag.id == id).first()
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    update_data = tag.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_tag, key, value)
    db.commit()
    db.refresh(db_tag)
    return db_tag

@router.delete("/{id}")
def delete_tag(id: int, db: Session = Depends(get_db)):
    db_tag = db.query(Tag).filter(Tag.id == id).first()
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    db.delete(db_tag)
    db.commit()
    return {"status": "deleted", "id": id}