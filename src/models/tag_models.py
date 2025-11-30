from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database.db import Base

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    userId = Column(Integer, nullable=False, index=True)
    movieId = Column(Integer, ForeignKey("movies.movieId"), nullable=False, index=True)
    tag = Column(String, nullable=False, index=True)
    timestamp = Column(BigInteger, nullable=False)

    movie = relationship("Movie", back_populates="tags")

    __table_args__ = (
        UniqueConstraint("userId", "movieId", "tag", "timestamp", name="uix_tag_full"),
    )