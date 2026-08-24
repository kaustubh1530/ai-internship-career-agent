import pytest
from backend.live_job_fetcher import normalize_job

def test_normalize_job_missing_job_title():
    raw_job = {}
    result = normalize_job(raw_job)
    assert result["title"] == "Untitled Job"

def test_normalize_job_missing_company():
    raw_job = {
        "title": "Python Intern"
    }
    result = normalize_job(raw_job)
    assert result["company"] == "Unknown Company"

def test_normalize_job_missing_description():
    raw_job = {
        "title": "Python Intern"
    }
    result = normalize_job(raw_job)
    assert result["description"] == ""

def test_normalize_job_missing_url():
    raw_job = {
        "title" : "Python Intern"
    }
    result = normalize_job(raw_job)
    assert result["url"] == "#"

def test_normalize_job_empty_job():
    raw_job = {}
    result = normalize_job(raw_job)
    assert result["title"] == "Untitled Job"
    assert result["company"] == "Unknown Company"

def test_normalize_job_title_is_none():
    raw_job = {
	    "title" : None
    }
    result = normalize_job(raw_job)
    assert result["title"] is None

def test_normalize_job_title_wrong_type():
    raw_job = {
        "title" : 12345
    }
    result = normalize_job(raw_job)
    assert result["title"] == 12345

def test_normalize_job_title_empty_string():
    raw_job = {
        "title" : ""
    }
    result = normalize_job(raw_job)
    assert result["title"] == ""



def test_normalize_job_valid_job():
    raw_job = {
        "title": "Python Intern",
        "company": {
            "display_name": "C4ADS"
        },
        "description": "Python development internship",
    }

    result = normalize_job(raw_job)

    assert result["title"] == "Python Intern"
    assert result["company"] == "C4ADS"
    assert result["description"] == "Python development internship"


def test_normalize_job_company_missing_display_name():
    raw_job = {
        "title": "Python Intern",
        "company": {},
        "description": "Python development internship",
    }
    result = normalize_job(raw_job)
    assert result["title"] == "Python Intern"
    assert result["company"] == "Unknown Company"
    assert result["description"] == "Python development internship"

def test_normalize_job_company_display_name_is_none():
    raw_job = {
            "title": "Python Intern",
            "company": {
                "display_name" : None            
            },
            "description": "Python development internship",
        }
    result = normalize_job(raw_job)
    assert result["title"] == "Python Intern"
    assert result["company"] is None
    assert result["description"] == "Python development internship"


def test_normalize_job_company_is_none():
    raw_job = {
    "title": "Python Intern",
    "company": None
}
    with pytest.raises(AttributeError):
        normalize_job(raw_job)

def test_normalize_job_company_is_none():
    raw_job = {
    "title": "Python Intern",
    "company": None
}
    result = normalize_job(raw_job)
    assert result["company"] == "Unknown Company"