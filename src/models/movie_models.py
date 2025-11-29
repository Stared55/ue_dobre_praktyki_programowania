from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.db import Base

from .link_models import *
from .rating_models import *
from .tag_models import *

class Movie(Base):
    __tablename__ = "movies"

    movieId = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    genres = Column(String, nullable=False)

    # Relationships
    links = relationship("Link", back_populates="movie")
    ratings = relationship("Rating", back_populates="movie")
    tags = relationship("Tag", back_populates="movie")
