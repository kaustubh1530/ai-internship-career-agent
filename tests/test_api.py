from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.api import app


client = TestClient(app)


@patch("backend.api.fetch_live_jobs")
def test_get_jobs(mock_fetch_live_jobs):
    mock_fetch_live_jobs.return_value = [
        {
            "title": "Python Intern",
            "company": "ABC Company",
            "location": "Maryland",
            "description": "Python development internship",
            "url": "https://example.com/job"
        }
    ]

    response = client.get(
        "/jobs",
        params={
            "role": "python",
            "location": "Maryland"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["role"] == "python"
    assert data["location"] == "Maryland"
    assert data["jobs"][0]["title"] == "Python Intern"

    mock_fetch_live_jobs.assert_called_once_with(
        role="python",
        location="Maryland"
    )

@patch("backend.api.fetch_live_jobs")
def test_get_jobs_service_unavailable(mock_fetch_live_jobs):
    mock_fetch_live_jobs.side_effect = RuntimeError(
        "Network request to job API failed"
    )

    response = client.get(
        "/jobs",
        params={
            "role": "python",
            "location": "Maryland"
        }
    )

    assert response.status_code == 503
    assert response.json() == {
        "detail": "Job service is temporarily unavailable"
    }

@patch("backend.api.fetch_live_jobs")
def test_get_jobs_rejects_short_role(mock_fetch_live_jobs):
    response = client.get(
        "/jobs",
        params={
            "role": "a",
            "location": "Maryland"
        }
    )

    assert response.status_code == 422
    mock_fetch_live_jobs.assert_not_called()

@patch("backend.api.fetch_live_jobs")
def test_get_jobs_response_structure(mock_fetch_live_jobs):
    mock_fetch_live_jobs.return_value = [
        {
            "title": "AI Engineer Intern",
            "company": "Example Company",
            "location": "Maryland",
            "description": "AI engineering internship",
            "url": "https://example.com/job"
        }
    ]

    response = client.get(
        "/jobs",
        params={
            "role": "ai",
            "location": "Maryland"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert set(data.keys()) == {
        "role",
        "location",
        "jobs"
    }

    assert isinstance(data["role"], str)
    assert isinstance(data["location"], str)
    assert isinstance(data["jobs"], list)
    