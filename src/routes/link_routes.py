from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from utils.session import get_db
from models.link_models import Link
from schemas.link_schemas import LinkSchema, LinkCreate, LinkUpdate
from schemas.pagination_schemas import PaginatedResponse

router = APIRouter(prefix="/links", tags=["Links"])

@router.get("/", response_model=PaginatedResponse[LinkSchema])
def get_links(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1), db: Session = Depends(get_db)):
    total = db.query(Link).count()
    items = db.query(Link).offset(skip).limit(limit).all()
    return PaginatedResponse(total=total, skip=skip, limit=limit, items=items)

@router.get("/{link_id}", response_model=LinkSchema)
def get_link(link_id: int, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.id == link_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link

@router.post("/", response_model=LinkSchema)
def create_link(link: LinkCreate, db: Session = Depends(get_db)):
    db_link = Link(**link.dict())
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link

@router.put("/{link_id}", response_model=LinkSchema)
def update_link(link_id: int, link: LinkUpdate, db: Session = Depends(get_db)):
    db_link = db.query(Link).filter(Link.id == link_id).first()
    if not db_link:
        raise HTTPException(status_code=404, detail="Link not found")
    for key, value in link.dict().items():
        setattr(db_link, key, value)
    db.commit()
    db.refresh(db_link)
    return db_link

@router.delete("/{link_id}")
def delete_link(link_id: int, db: Session = Depends(get_db)):
    db_link = db.query(Link).filter(Link.id == link_id).first()
    if not db_link:
        raise HTTPException(status_code=404, detail="Link not found")
    db.delete(db_link)
    db.commit()
    return {"status": "deleted"}