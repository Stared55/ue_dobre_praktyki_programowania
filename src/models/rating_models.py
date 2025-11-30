from sqlalchemy import Column, Integer, Float, BigInteger, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database.db import Base

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    userId = Column(Integer, nullable=False, index=True)
    movieId = Column(Integer, ForeignKey("movies.movieId"), nullable=False, index=True)

    rating = Column(Float, nullable=False)
    timestamp = Column(BigInteger, nullable=False)

    movie = relationship("Movie", back_populates="ratings")

    __table_args__ = (
        UniqueConstraint("userId", "movieId", name="uix_user_movie"),
    )