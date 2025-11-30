from pydantic import BaseModel

class MovieCreate(BaseModel):
    title: str
    genres: str

class MovieUpdate(BaseModel):
    title: str | None = None
    genres: str | None = None

class MovieSchema(BaseModel):
    movieId: int
    title: str
    genres: str

    model_config = {
        "from_attributes": True
    }