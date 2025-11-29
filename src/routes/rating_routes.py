from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from utils.session import get_db
from models.rating_models import Rating

router = APIRouter(
    prefix='/ratings',
    tags=["Ratings"],
)

@router.get("/")
def get_all_ratings(db: Session = Depends(get_db)):
    return db.query(Rating).all()


@router.get("/{rating_id}")
def get_rating_by_id(rating_id: int, db: Session = Depends(get_db)):
    rating = db.query(Rating).filter(Rating.ratingId == rating_id).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    return rating