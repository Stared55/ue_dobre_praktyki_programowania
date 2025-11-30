from models.tag_models import Tag

def test_get_all_tags(client, sample_tags):
    response = client.get("/tags/")
    assert response.status_code == 200

    data = response.json()
    assert data["total"] == len(sample_tags)
    assert len(data["items"]) == len(sample_tags)


def test_get_tag_by_id(client, sample_tags):
    tag_id = sample_tags[0].id

    response = client.get(f"/tags/{tag_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == tag_id
    assert data["userId"] == sample_tags[0].userId
    assert data["movieId"] == sample_tags[0].movieId
    assert data["tag"] == sample_tags[0].tag
    assert data["timestamp"] == sample_tags[0].timestamp


def test_get_tag_not_found(client):
    response = client.get("/tags/9999")
    assert response.status_code == 404


def test_create_tag(client, db_session):
    payload = {"userId": 3, "movieId": 3, "tag": "Horror", "timestamp": 1234567890}

    response = client.post("/tags/", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["userId"] == 3
    assert data["movieId"] == 3
    assert data["tag"] == "Horror"
    assert data["timestamp"] == 1234567890

    created = db_session.query(Tag).filter_by(id=data["id"]).first()
    assert created is not None
    assert created.tag == "Horror"


def test_update_tag(client, db_session, sample_tags):
    tag_id = sample_tags[0].id
    payload = {"tag": "Comedy", "timestamp": 987654321}

    response = client.put(f"/tags/{tag_id}", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["tag"] == "Comedy"
    assert data["timestamp"] == 987654321

    updated = db_session.query(Tag).filter_by(id=tag_id).first()
    assert updated.tag == "Comedy"
    assert updated.timestamp == 987654321


def test_delete_tag(client, db_session, sample_tags):
    tag_id = sample_tags[0].id

    response = client.delete(f"/tags/{tag_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "deleted"

    deleted = db_session.query(Tag).filter_by(id=tag_id).first()
    assert deleted is None