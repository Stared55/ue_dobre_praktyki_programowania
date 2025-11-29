from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from utils.session import get_db
from models.movie_models import Rating
from utils.pagination import pagination_params

router = APIRouter(prefix="/ratings", tags=["Ratings"])

@router.get("/")
def get_all_ratings(
    pagination: tuple[int, int] = Depends(pagination_params),
    db: Session = Depends(get_db)
):
    skip, limit = pagination
    ratings = db.query(Rating).offset(skip).limit(limit).all()
    return {"skip": skip, "limit": limit, "count": len(ratings), "ratings": ratings}


@router.get("/{user_id}/{movie_id}")
def get_rating_by_id(user_id: int, movie_id: int, db: Session = Depends(get_db)):
    rating = db.query(Rating).filter(
        Rating.userId == user_id,
        Rating.movieId == movie_id
    ).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    return rating