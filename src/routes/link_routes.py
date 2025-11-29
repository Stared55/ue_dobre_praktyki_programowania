from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from utils.session import get_db
from models.movie_models import Link
from utils.pagination import pagination_params

router = APIRouter(prefix="/links", tags=["Links"])

@router.get("/")
def get_all_links(
    pagination: tuple[int, int] = Depends(pagination_params),
    db: Session = Depends(get_db)
):
    skip, limit = pagination
    links = db.query(Link).offset(skip).limit(limit).all()
    return {"skip": skip, "limit": limit, "count": len(links), "links": links}


@router.get("/{link_id}")
def get_link_by_id(link_id: int, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.id == link_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link