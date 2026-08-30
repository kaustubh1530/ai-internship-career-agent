from unittest.mock import Mock
from unittest.mock import patch
import pytest
import requests
from backend.live_job_fetcher import fetch_live_jobs
@patch("backend.live_job_fetcher.requests.get")
def test_fetch_live_jobs(mock_get):

    mock_response = Mock()

    mock_response.status_code = 200
    mock_get.return_value = mock_response

    mock_response.json.return_value = {
    "results": [
        {
            "title": "Python Intern",
            "company": {"display_name": "ABC Company"},
            "location": {"display_name": "Maryland"},
            "description": "Python development internship",
            "redirect_url": "https://example.com/job"
        }
    ]
}


    result = fetch_live_jobs()

    assert result[0]["title"] == "Python Intern"





from unittest.mock import Mock
from unittest.mock import patch
from backend.live_job_fetcher import fetch_live_jobs
import pytest


@patch("backend.live_job_fetcher.requests.get")
def test_fetch_live_jobs_api_failure(mock_get):
    mock_response = Mock()

    mock_response.status_code = 500
    mock_get.return_value = mock_response

    mock_response.json.return_value = {
    "results": [
        {
            "title": "Python Intern",
            "company": {"display_name": "ABC Company"},
            "location": {"display_name": "Maryland"},
            "description": "Python development internship",
            "redirect_url": "https://example.com/job"
        }
    ]
}

    with pytest.raises(RuntimeError):
        fetch_live_jobs()

@patch("backend.live_job_fetcher.requests.get")
def test_fetch_live_jobs_network_failure(mock_get):
    mock_get.side_effect = requests.exceptions.RequestException("Network error")

    with pytest.raises(RuntimeError):
        fetch_live_jobs()


@patch("backend.live_job_fetcher.get_secret")
def test_fetch_live_jobs_missing_credentials(mock_get_secret):
    mock_get_secret.return_value = None

    with pytest.raises(ValueError, match="Missing ADZUNA_APP_ID or ADZUNA_APP_KEY"):
        fetch_live_jobs()
