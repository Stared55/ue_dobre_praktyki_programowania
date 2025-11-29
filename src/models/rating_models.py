from sqlalchemy import Column, Integer, Float, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from database.db import Base
 
class Rating(Base):
    __tablename__ = "ratings"

    # Composite key: userId + movieId
    userId = Column(Integer, primary_key=True)
    movieId = Column(Integer, ForeignKey("movies.movieId"), primary_key=True)

    rating = Column(Float, nullable=False)
    timestamp = Column(BigInteger, nullable=False)

    movie = relationship("Movie", back_populates="ratings")
