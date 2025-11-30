from models.movie_models import Movie

def test_get_all_movies(client, sample_movies):
    response = client.get("/movies/")
    assert response.status_code == 200

    data = response.json()
    assert data["total"] == len(sample_movies)
    assert len(data["items"]) == len(sample_movies)

def test_get_movie_by_id(client, sample_movies):
    movie_id = sample_movies[0].movieId
    response = client.get(f"/movies/{movie_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["movieId"] == movie_id
    assert data["title"] == sample_movies[0].title
    assert data["genres"] == sample_movies[0].genres

def test_get_movie_not_found(client):
    response = client.get("/movies/9999")
    assert response.status_code == 404

def test_create_movie(client, db_session):
    payload = {"title": "New Movie", "genres": "Horror"}
    response = client.post("/movies/", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "New Movie"
    assert data["genres"] == "Horror"

    created = db_session.query(Movie).filter_by(movieId=data["movieId"]).first()
    assert created is not None
    assert created.title == "New Movie"

def test_update_movie(client, db_session, sample_movies):
    movie_id = sample_movies[0].movieId
    payload = {"title": "Updated Title", "genres": "Thriller"}

    response = client.put(f"/movies/{movie_id}", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["genres"] == "Thriller"

    updated = db_session.query(Movie).filter_by(movieId=movie_id).first()
    assert updated.title == "Updated Title"
    assert updated.genres == "Thriller"

def test_delete_movie(client, db_session, sample_movies):
    movie_id = sample_movies[0].movieId
    response = client.delete(f"/movies/{movie_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "deleted"

    deleted = db_session.query(Movie).filter_by(movieId=movie_id).first()
    assert deleted is None