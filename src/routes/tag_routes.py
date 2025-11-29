from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from utils.session import get_db
from models.tag_models import Tag
from utils.pagination import pagination_params

router = APIRouter(prefix="/tags", tags=["Tags"])

@router.get("/")
def get_all_tags(
    pagination: tuple[int, int] = Depends(pagination_params),
    db: Session = Depends(get_db)
):
    skip, limit = pagination
    tags = db.query(Tag).offset(skip).limit(limit).all()
    return {"skip": skip, "limit": limit, "count": len(tags), "tags": tags}


@router.get("/{user_id}/{movie_id}/{tag_value}/{timestamp}")
def get_tag_by_id(user_id: int, movie_id: int, tag_value: str, timestamp: int, db: Session = Depends(get_db)):
    tag = db.query(Tag).filter(
        Tag.userId == user_id,
        Tag.movieId == movie_id,
        Tag.tag == tag_value,
        Tag.timestamp == timestamp
    ).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag