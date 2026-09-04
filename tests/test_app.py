from fastapi.testclient import TestClient

from src import app as app_module

client = TestClient(app_module.app)


def test_unregister_removes_participant_from_activity():
    app_module.activities["Chess Club"]["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]

    response = client.delete(
        "/activities/Chess Club/unregister?email=michael@mergington.edu"
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["message"] == "Unregistered michael@mergington.edu from Chess Club"
    assert "michael@mergington.edu" not in app_module.activities["Chess Club"]["participants"]


def test_unregister_missing_participant_raises_error():
    app_module.activities["Chess Club"]["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]

    response = client.delete(
        "/activities/Chess Club/unregister?email=unknown@mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found in this activity"
