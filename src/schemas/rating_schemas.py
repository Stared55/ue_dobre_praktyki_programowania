from pydantic import BaseModel

class RatingBase(BaseModel):
    userId: int
    movieId: int
    rating: float
    timestamp: int

class RatingCreate(RatingBase):
    pass

class RatingUpdate(BaseModel):
    rating: float | None = None
    timestamp: int | None = None

class RatingSchema(RatingBase):
    id: int

    model_config = {
        "from_attributes": True
    }