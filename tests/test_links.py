from models.link_models import Link


def test_get_all_links(client, sample_links):
    response = client.get("/links/")
    assert response.status_code == 200

    data = response.json()
    assert data["total"] == len(sample_links)
    assert len(data["items"]) == len(sample_links)


def test_get_link_by_id(client, sample_links):
    link_id = sample_links[0].id

    response = client.get(f"/links/{link_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == link_id
    assert data["movieId"] == sample_links[0].movieId
    assert data["imdbId"] == sample_links[0].imdbId


def test_get_link_not_found(client):
    response = client.get("/links/9999")
    assert response.status_code == 404


def test_create_link(client, db_session):
    payload = {
        "movieId": 10,
        "imdbId": 555,
        "tmdbId": 777
    }

    response = client.post("/links/", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["movieId"] == 10
    assert data["imdbId"] == 555

    created = db_session.query(Link).filter_by(movieId=10).first()
    assert created is not None
    assert created.tmdbId == 777


def test_update_link(client, db_session, sample_links):
    link_id = sample_links[0].id
    payload = {"imdbId": 999, "tmdbId": 888}

    response = client.put(f"/links/{link_id}", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["imdbId"] == 999
    assert data["tmdbId"] == 888

    updated = db_session.query(Link).filter_by(id=link_id).first()
    assert updated.imdbId == 999
    assert updated.tmdbId == 888


def test_delete_link(client, db_session, sample_links):
    link_id = sample_links[0].id

    response = client.delete(f"/links/{link_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "deleted"

    deleted = db_session.query(Link).filter_by(id=link_id).first()
    assert deleted is None