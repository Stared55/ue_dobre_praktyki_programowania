from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from utils.session import get_db
from models.link_models import Link

router = APIRouter(
    prefix='/links',
    tags=["Links"],
)

@router.get("/")
def get_all_links(db: Session = Depends(get_db)):
    return db.query(Link).all()


@router.get("/{link_id}")
def get_link_by_id(link_id: int, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.linkId == link_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link