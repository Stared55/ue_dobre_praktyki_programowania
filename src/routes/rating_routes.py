from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Tuple

from utils.session import get_db
from models.rating_models import Rating
from schemas.rating_schemas import RatingSchema, RatingCreate, RatingUpdate
from schemas.pagination_schemas import PaginatedResponse
from utils.pagination import pagination_params

router = APIRouter(prefix="/ratings", tags=["Ratings"])

@router.get("/", response_model=PaginatedResponse[RatingSchema])
def get_all_ratings(pagination: Tuple[int, int] = Depends(pagination_params), db: Session = Depends(get_db)):
    skip, limit = pagination
    total = db.query(Rating).count()
    items = db.query(Rating).offset(skip).limit(limit).all()
    return PaginatedResponse(total=total, skip=skip, limit=limit, items=items)

@router.get("/{id}", response_model=RatingSchema)
def get_rating_by_id(id: int, db: Session = Depends(get_db)):
    rating = db.query(Rating).filter(Rating.id == id).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    return rating

@router.post("/", response_model=RatingSchema)
def create_rating(rating: RatingCreate, db: Session = Depends(get_db)):
    db_rating = Rating(**rating.model_dump())
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

@router.put("/{id}", response_model=RatingSchema)
def update_rating(id: int, rating: RatingUpdate, db: Session = Depends(get_db)):
    db_rating = db.query(Rating).filter(Rating.id == id).first()
    if not db_rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    update_data = rating.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_rating, key, value)
    db.commit()
    db.refresh(db_rating)
    return db_rating

@router.delete("/{id}")
def delete_rating(id: int, db: Session = Depends(get_db)):
    db_rating = db.query(Rating).filter(Rating.id == id).first()
    if not db_rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    db.delete(db_rating)
    db.commit()
    return {"status": "deleted", "id": id}