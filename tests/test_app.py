import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
        }
    }
    yield


@pytest.fixture
def client():
    return TestClient(app_module.app)


def test_unregister_participant_removes_email_from_activity(client):
    response = client.delete("/activities/Chess Club/participants/michael@mergington.edu")

    assert response.status_code == 200
    assert "michael@mergington.edu" not in app_module.activities["Chess Club"]["participants"]
    assert "daniel@mergington.edu" in app_module.activities["Chess Club"]["participants"]


def test_unregister_participant_returns_not_found_when_missing(client):
    response = client.delete("/activities/Chess Club/participants/ghost@mergington.edu")

    assert response.status_code == 404
