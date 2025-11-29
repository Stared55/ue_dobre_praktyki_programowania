from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from utils.session import get_db
from models.tag_models import Tag

router = APIRouter(
    prefix='/tags',
    tags=["Tags"],
)

@router.get("/")
def get_all_tags(db: Session = Depends(get_db)):
    return db.query(Tag).all()


@router.get("/{tag_id}")
def get_tag_by_id(tag_id: int, db: Session = Depends(get_db)):
    tag = db.query(Tag).filter(Tag.tagId == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag