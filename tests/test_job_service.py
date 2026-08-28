import pytest
from unittest.mock import patch

from backend.services.job_service import get_jobs


@patch("backend.services.job_service.fetch_live_jobs")
def test_get_jobs_calls_fetcher(mock_fetch_live_jobs):
    mock_fetch_live_jobs.return_value = [
        {
            "title": "Python Intern",
            "company": "Test Company",
            "location": "Maryland",
            "description": "Python internship",
            "url": "https://example.com/job"
        }
    ]

    result = get_jobs(
        role="python",
        location="Maryland"
    )

    mock_fetch_live_jobs.assert_called_once_with(
        role="python",
        location="Maryland"
    )

    assert result == mock_fetch_live_jobs.return_value

@patch("backend.services.job_service.fetch_live_jobs")
def test_get_jobs_propagates_fetcher_error(mock_fetch_live_jobs):
    mock_fetch_live_jobs.side_effect = RuntimeError(
        "Network request to job API failed"
    )

    with pytest.raises(
        RuntimeError,
        match="Network request to job API failed"
    ):
        get_jobs(
            role="python",
            location="Maryland"
        )