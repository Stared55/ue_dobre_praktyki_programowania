from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    movieId = Column(Integer, ForeignKey("movies.movieId"), nullable=False)
    imdbId = Column(Integer, nullable=True)
    tmdbId = Column(Integer, nullable=True)

    movie = relationship("Movie", back_populates="links")