import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.db import Base
from main import app
from utils.session import get_db
from models.movie_models import Movie, Link, Rating, Tag

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def sample_movies(db_session):
    movies = [
        Movie(movieId=1, title="Movie 1", genres="Action"),
        Movie(movieId=2, title="Movie 2", genres="Comedy"),
    ]
    db_session.add_all(movies)
    db_session.commit()
    return movies

@pytest.fixture
def sample_links(db_session, sample_movies):
    links = [
        Link(id=1, movieId=1, imdbId=101, tmdbId=201),
        Link(id=2, movieId=2, imdbId=102, tmdbId=202),
    ]
    db_session.add_all(links)
    db_session.commit()
    return links

@pytest.fixture
def sample_ratings(db_session, sample_movies):
    ratings = [
        Rating(userId=1, movieId=1, rating=4.5, timestamp=1700000000),
        Rating(userId=2, movieId=2, rating=3.0, timestamp=1700000100),
    ]
    db_session.add_all(ratings)
    db_session.commit()
    return ratings

@pytest.fixture
def sample_tags(db_session, sample_movies):
    tags = [
        Tag(userId=1, movieId=1, tag="fun", timestamp=1700000000),
        Tag(userId=2, movieId=2, tag="serious", timestamp=1700000100),
    ]
    db_session.add_all(tags)
    db_session.commit()
    return tags