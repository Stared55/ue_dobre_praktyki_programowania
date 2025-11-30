from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Tuple

from utils.session import get_db
from models.movie_models import Movie
from schemas.movie_schemas import MovieSchema, MovieCreate, MovieUpdate
from schemas.pagination_schemas import PaginatedResponse
from utils.pagination import pagination_params

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.get("/", response_model=PaginatedResponse[MovieSchema])
def get_all_movies(pagination: Tuple[int, int] = Depends(pagination_params), db: Session = Depends(get_db)):
    skip, limit = pagination
    total = db.query(Movie).count()
    items = db.query(Movie).offset(skip).limit(limit).all()
    return PaginatedResponse(total=total, skip=skip, limit=limit, items=items)

@router.get("/{movie_id}", response_model=MovieSchema)
def get_movie_by_id(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.movieId == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.post("/", response_model=MovieSchema)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    db_movie = Movie(**movie.model_dump())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@router.put("/{movie_id}", response_model=MovieSchema)
def update_movie(movie_id: int, movie: MovieUpdate, db: Session = Depends(get_db)):
    db_movie = db.query(Movie).filter(Movie.movieId == movie_id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    update_data = movie.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_movie, key, value)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@router.delete("/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = db.query(Movie).filter(Movie.movieId == movie_id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    db.delete(db_movie)
    db.commit()
    return {"status": "deleted", "id": movie_id}