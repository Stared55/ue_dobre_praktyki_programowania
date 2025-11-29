from models.movie_models import Movie

def test_get_all_movies(client, sample_movies):
    response = client.get("/movies/")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == len(sample_movies)
    assert len(data["movies"]) == len(sample_movies)

def test_get_movie_by_id(client, sample_movies):
    movie_id = sample_movies[0].movieId
    response = client.get(f"/movies/{movie_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["movieId"] == movie_id
    assert data["title"] == sample_movies[0].title

def test_get_movie_not_found(client):
    response = client.get("/movies/9999")
    assert response.status_code == 404

def test_create_movie(client, db_session):
    payload = {"movieId": 3, "title": "New Movie", "genres": "Horror"}
    response = client.post("/movies/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Movie"

    movie_in_db = db_session.query(Movie).filter_by(movieId=3).first()
    assert movie_in_db is not None
    assert movie_in_db.genres == "Horror"

def test_update_movie(client, db_session, sample_movies):
    movie_id = sample_movies[0].movieId
    payload = {"title": "Updated Movie", "genres": "Thriller"}
    response = client.put(f"/movies/{movie_id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Movie"

    movie_in_db = db_session.query(Movie).filter_by(movieId=movie_id).first()
    assert movie_in_db.genres == "Thriller"

def test_delete_movie(client, db_session, sample_movies):
    movie_id = sample_movies[0].movieId
    response = client.delete(f"/movies/{movie_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "deleted"

    movie_in_db = db_session.query(Movie).filter_by(movieId=movie_id).first()
    assert movie_in_db is None