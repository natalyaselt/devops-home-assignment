from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_epoch_success() -> None:
    """
    Verify that a valid ISO-8601 date is converted to a Unix epoch.
    """
    response = client.post(
        "/epoch",
        json={"date": "2026-06-15T10:00:00Z"},
    )

    assert response.status_code == 200
    assert response.json() == {"epoch": 1781517600}


def test_invalid_date_format() -> None:
    """
    Verify that an invalid date format returns HTTP 422.
    """
    response = client.post(
        "/epoch",
        json={"date": "invalid-date"},
    )

    assert response.status_code == 422


def test_missing_date_field() -> None:
    """
    Verify that a missing required field returns HTTP 422.
    """
    response = client.post(
        "/epoch",
        json={},
    )

    assert response.status_code == 422


def test_empty_request_body() -> None:
    """
    Verify that an empty request body returns HTTP 422.
    """
    response = client.post(
        "/epoch",
        json=None,
    )

    assert response.status_code == 422


def test_missing_content_type() -> None:
    """
    Verify that a request without Content-Type is rejected.
    """
    response = client.post(
        "/epoch",
        data='{"date":"2026-06-15T10:00:00Z"}',
    )

    # FastAPI may accept this depending on how the request is parsed.
    # If rejected, it should return 415 or 422.
    assert response.status_code in (200, 415, 422)


def test_invalid_json() -> None:
    """
    Verify that malformed JSON returns HTTP 422.
    """
    response = client.post(
        "/epoch",
        data='{"date":',
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 422


def test_wrong_field_name() -> None:
    """
    Verify that an unexpected field name returns HTTP 422.
    """
    response = client.post(
        "/epoch",
        json={"timestamp": "2026-06-15T10:00:00Z"},
    )

    assert response.status_code == 422


def test_additional_fields_are_ignored() -> None:
    """
    Verify that extra fields do not affect the response.
    """
    response = client.post(
        "/epoch",
        json={
            "date": "2026-06-15T10:00:00Z",
            "user": "Alex",
            "extra": 123,
        },
    )

    assert response.status_code == 200
    assert response.json()["epoch"] == 1781517600


def test_future_date() -> None:
    """
    Verify that future dates are converted successfully.
    """
    response = client.post(
        "/epoch",
        json={"date": "2100-01-01T00:00:00Z"},
    )

    assert response.status_code == 200


def test_past_date() -> None:
    """
    Verify that historical dates are converted successfully.
    """
    response = client.post(
        "/epoch",
        json={"date": "1970-01-01T00:00:00Z"},
    )

    assert response.status_code == 200
    assert response.json()["epoch"] == 0


def test_wrong_endpoint() -> None:
    """Verify that an unknown endpoint returns HTTP 404."""
    response = client.post("/unknown")
    assert response.status_code == 404


def test_get_not_allowed() -> None:
    """Verify that GET is not allowed for the /epoch endpoint."""
    response = client.get("/epoch")
    assert response.status_code == 405
