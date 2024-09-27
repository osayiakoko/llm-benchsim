from pytest import MonkeyPatch
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.models import BenchmarkResult


def test_get_benchmark(
    db_session: Session, client: TestClient, monkeypatch: MonkeyPatch
):
    """
    Test the GET /api/v1/benchmark/{metric} endpoint by seeding the database with test data,
    making a request to the endpoint, and asserting the response.

    Args:
        db_session (Session): The SQLAlchemy session object used to interact with the database.
        client (TestClient): The FastAPI test client used to make HTTP requests.

    Returns:
        None
    """

    monkeypatch.setattr("src.core.cache.RedisCache.get", lambda *args, **kwargs: None)
    monkeypatch.setattr("src.core.cache.RedisCache.set", lambda *args, **kwargs: None)

    # Seed the database with test data
    benchmark = BenchmarkResult(
        metric="TTFT",
        llm_name="GPT-3",
        mean_value=0.5,
        rank=1,
    )
    db_session.add(benchmark)
    db_session.commit()

    response = client.get("/api/v1/benchmark/TTFT")
    assert response.status_code == 200
    res_data = response.json()["data"]
    assert len(res_data) == 1
    assert res_data[0]["metric"] == "TTFT"
    assert res_data[0]["llm_name"] == "GPT-3"
    assert res_data[0]["mean_value"] == 0.5
    assert res_data[0]["rank"] == 1


def test_get_benchmark_not_found(client: TestClient):
    """
    Tests the GET /benchmark/{metric} endpoint with a non-existent metric.

    Args:
        client (TestClient): The FastAPI test client used to make HTTP requests.

    Returns:
        None
    """
    response = client.get("/benchmark/NONEXISTENT")
    assert response.status_code == 404


def test_invalid_api_key(client: TestClient):
    """
    Tests the GET /api/v1/benchmark/{metric} endpoint with an invalid API key.

    Args:
        client (TestClient): The FastAPI test client used to make HTTP requests.

    Returns:
        None
    """
    response = client.get("/api/v1/benchmark/TTFT", headers={"X-API-Key": "invalid"})
    assert response.status_code == 403
    assert response.json()["message"] == "Could not validate API key"
