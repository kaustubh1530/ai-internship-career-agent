from fastapi.testclient import TestClient

from backend.api import app, get_job_service


client = TestClient(app)


def test_get_jobs():
    def fake_job_service(role, location):
        return [
            {
                "title": "Python Intern",
                "company": "ABC Company",
                "location": "Maryland",
                "description": "Python development internship",
                "url": "https://example.com/job"
            }
        ]

    def fake_dependency():
        return fake_job_service

    app.dependency_overrides[get_job_service] = fake_dependency

    try:
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

    finally:
        app.dependency_overrides.clear()


def test_get_jobs_service_unavailable():
    def fake_job_service(role, location):
        raise RuntimeError(
            "Network request to job API failed"
        )

    def fake_dependency():
        return fake_job_service

    app.dependency_overrides[get_job_service] = fake_dependency

    try:
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

    finally:
        app.dependency_overrides.clear()


def test_get_jobs_rejects_short_role():
    def fake_job_service(role, location):
        return []

    def fake_dependency():
        return fake_job_service

    app.dependency_overrides[get_job_service] = fake_dependency

    try:
        response = client.get(
            "/jobs",
            params={
                "role": "a",
                "location": "Maryland"
            }
        )

        assert response.status_code == 422

    finally:
        app.dependency_overrides.clear()


def test_get_jobs_response_structure():
    def fake_job_service(role, location):
        return [
            {
                "title": "AI Engineer Intern",
                "company": "Example Company",
                "location": "Maryland",
                "description": "AI engineering internship",
                "url": "https://example.com/job"
            }
        ]

    def fake_dependency():
        return fake_job_service

    app.dependency_overrides[get_job_service] = fake_dependency

    try:
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

    finally:
        app.dependency_overrides.clear()


def test_get_jobs_with_fake_dependency():
    def fake_job_service(role, location):
        return [
            {
                "title": "Fake AI Intern",
                "company": "Test Company",
                "location": location,
                "description": "Fake job for testing",
                "url": "https://example.com/fake-job"
            }
        ]

    def fake_dependency():
        return fake_job_service

    app.dependency_overrides[get_job_service] = fake_dependency

    try:
        response = client.get(
            "/jobs",
            params={
                "role": "ai",
                "location": "Maryland"
            }
        )

        assert response.status_code == 200

        data = response.json()

        assert data["role"] == "ai"
        assert data["location"] == "Maryland"
        assert data["jobs"][0]["title"] == "Fake AI Intern"

    finally:
        app.dependency_overrides.clear()