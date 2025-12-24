from fastapi.testclient import TestClient
from src.app import app
import uuid
import urllib.parse

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "art Club"
    email = f"test+{uuid.uuid4().hex}@example.com"

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={urllib.parse.quote(email, safe='@')}")
    assert resp.status_code == 200

    # Confirm participant present
    resp = client.get("/activities")
    data = resp.json()
    participants = data.get(activity, {}).get("participants", [])
    assert email in participants

    # Unregister
    resp = client.delete(f"/activities/{activity}/signup?email={urllib.parse.quote(email, safe='@')}")
    assert resp.status_code == 200

    # Confirm removal
    resp = client.get("/activities")
    data = resp.json()
    participants = data.get(activity, {}).get("participants", [])
    assert email not in participants


def test_duplicate_signup_returns_400_and_cleanup():
    activity = "art Club"
    email = f"dup+{uuid.uuid4().hex}@example.com"

    # First signup
    resp1 = client.post(f"/activities/{activity}/signup?email={urllib.parse.quote(email, safe='@')}")
    assert resp1.status_code == 200

    # Duplicate signup should 400
    resp2 = client.post(f"/activities/{activity}/signup?email={urllib.parse.quote(email, safe='@')}")
    assert resp2.status_code == 400

    # Cleanup
    resp3 = client.delete(f"/activities/{activity}/signup?email={urllib.parse.quote(email, safe='@')}")
    assert resp3.status_code == 200
