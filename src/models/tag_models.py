from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from database.db import Base

class Tag(Base):
    __tablename__ = "tags"

    # Composite key: userId + movieId + tag + timestamp
    userId = Column(Integer, primary_key=True)
    movieId = Column(Integer, ForeignKey("movies.movieId"), primary_key=True)
    tag = Column(String, primary_key=True)
    timestamp = Column(BigInteger, primary_key=True)

    movie = relationship("Movie", back_populates="tags")