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