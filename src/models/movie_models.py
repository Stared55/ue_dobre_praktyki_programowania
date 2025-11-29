from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.db import Base

class Movie(Base):
    __tablename__ = "movies"

    movieId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    genres = Column(String, nullable=False)

    links = relationship("Link", back_populates="movie", cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="movie", cascade="all, delete-orphan")
    tags = relationship("Tag", back_populates="movie", cascade="all, delete-orphan")