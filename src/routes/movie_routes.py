from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.session import get_db
from models.movie_models import Movie
from utils.pagination import pagination_params  # import the dependency

router = APIRouter(
    prefix='/movies',
    tags=["Movies"],
)

@router.get("/")
def get_all_movies(
    pagination: tuple[int, int] = Depends(pagination_params),
    db: Session = Depends(get_db)
):
    skip, limit = pagination
    movies = db.query(Movie).offset(skip).limit(limit).all()
    return {
        "skip": skip,
        "limit": limit,
        "count": len(movies),
        "movies": movies
    }

@router.get("/{movie_id}")
def get_movie_by_id(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.movieId == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie