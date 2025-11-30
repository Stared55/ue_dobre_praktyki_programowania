from pydantic import BaseModel
from typing import Optional

class LinkBase(BaseModel):
    movieId: int
    imdbId: Optional[int]
    tmdbId: Optional[int]

class LinkCreate(LinkBase):
    pass

class LinkUpdate(LinkBase):
    movieId: Optional[int] = None
    imdbId: Optional[int] = None
    tmdbId: Optional[int] = None

class LinkSchema(LinkBase):
    id: int

    class Config:
        orm_mode = True