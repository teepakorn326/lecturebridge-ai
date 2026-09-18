from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_lecture():

    response = client.post(
        "/api/v1/lectures",
        json={
            "title": "COMP8460 Week 7",
            "target_language": "th",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "COMP8460 Week 7"
    assert data["target_language"] == "th"
    assert data["status"] == "created"
    assert data["id"] is not None


def test_invalid_target_language():

    response = client.post(
        "/api/v1/lectures",
        json={
            "title": "COMP8460",
            "target_language": "japanese",
        },
    )

    assert response.status_code == 422


def test_get_missing_lecture():

    lecture_id = uuid4()

    response = client.get(
        f"/api/v1/lectures/{lecture_id}"
    )

    assert response.status_code == 404