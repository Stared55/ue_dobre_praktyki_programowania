from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Tuple

from utils.session import get_db
from utils.pagination import pagination_params
from models.movie_models import Movie

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.get("/")
def get_all_movies(
    pagination: Tuple[int, int] = Depends(pagination_params),
    db: Session = Depends(get_db)
):
    skip, limit = pagination
    movies = db.query(Movie).offset(skip).limit(limit).all()
    return {"skip": skip, "limit": limit, "count": len(movies), "movies": movies}

@router.get("/{movie_id}")
def get_movie_by_id(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.movieId == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.post("/")
def create_movie(payload: dict, db: Session = Depends(get_db)):
    movie = Movie(**payload)
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie

@router.put("/{movie_id}")
def update_movie(movie_id: int, payload: dict, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.movieId == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    movie.title = payload.get("title", movie.title)
    movie.genres = payload.get("genres", movie.genres)
    db.commit()
    db.refresh(movie)
    return movie

@router.delete("/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.movieId == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    db.delete(movie)
    db.commit()
    return {"status": "deleted"}