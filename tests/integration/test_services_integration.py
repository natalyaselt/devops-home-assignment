import requests


BASE_NOW = "http://localhost:8080"
BASE_EPOCH = "http://localhost:8081"


def test_epoch_contract_direct():
    """
    Contract test: epoch-service works over HTTP
    """
    response = requests.post(
        f"{BASE_EPOCH}/epoch",
        json={"date": "2026-06-15T10:00:00Z"},
        timeout=5,
    )

    assert response.status_code == 200
    assert "epoch" in response.json()


def test_service_to_service_flow():
    """
    End-to-end test: now-service -> epoch-service
    """
    response = requests.get(f"{BASE_NOW}/now", timeout=5)

    assert response.status_code == 200
    assert "message" in response.json()


def test_epoch_service_failure_behavior():
    """
    Simulates failure behavior (run manually with epoch-service stopped)
    """
    try:
        response = requests.get(f"{BASE_NOW}/now", timeout=5)
        assert response.status_code in (500, 503)
    except requests.exceptions.ConnectionError:
        # acceptable when service is down
        assert True


def test_full_service_flow():
    """
    Real integration test:
    now-time-service -> epoch-service
    """

    response = requests.get("http://localhost:8080/now", timeout=5)

    assert response.status_code == 200

    data = response.json()

    assert "message" in data
    assert "now is" in data["message"]

    # ensure numeric epoch exists in response
    assert any(char.isdigit() for char in data["message"])


def test_epoch_direct_contract():
    response = requests.post(
        "http://localhost:8081/epoch",
        json={"date": "2026-06-15T10:00:00Z"},
        timeout=5,
    )

    assert response.status_code == 200
    assert "epoch" in response.json()
