from models.rating_models import Rating


def test_get_all_ratings(client, sample_ratings):
    response = client.get("/ratings/")
    assert response.status_code == 200
    data = response.json()

    assert data["total"] == len(sample_ratings)
    assert len(data["items"]) == len(sample_ratings)


def test_get_rating_by_id(client, sample_ratings):
    rating_id = 1  # first fixture row
    response = client.get(f"/ratings/{rating_id}")
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == rating_id
    assert data["userId"] == sample_ratings[0].userId
    assert data["movieId"] == sample_ratings[0].movieId


def test_get_rating_not_found(client):
    response = client.get("/ratings/9999")
    assert response.status_code == 404


def test_create_rating(client, db_session):
    payload = {
        "userId": 3,
        "movieId": 1,
        "rating": 5.0,
        "timestamp": 1700000200
    }

    response = client.post("/ratings/", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["userId"] == 3
    assert data["rating"] == 5.0

    db_item = db_session.query(Rating).filter_by(userId=3, movieId=1).first()
    assert db_item is not None
    assert db_item.rating == 5.0


def test_update_rating(client, db_session, sample_ratings):
    rating_id = 1
    payload = {"rating": 1.0}

    response = client.put(f"/ratings/{rating_id}", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["rating"] == 1.0

    db_item = db_session.query(Rating).filter_by(id=rating_id).first()
    assert db_item.rating == 1.0


def test_delete_rating(client, db_session, sample_ratings):
    rating_id = 1

    response = client.delete(f"/ratings/{rating_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "deleted"

    db_item = db_session.query(Rating).filter_by(id=rating_id).first()
    assert db_item is None