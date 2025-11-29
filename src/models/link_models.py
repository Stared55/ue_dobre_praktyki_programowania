from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database.db import Base

class Link(Base):
    __tablename__ = "links"

    movieId = Column(Integer, ForeignKey("movies.movieId"), primary_key=True)
    imdbId = Column(Integer, nullable=True)
    tmdbId = Column(Integer, nullable=True)

    movie = relationship("Movie", back_populates="links")
