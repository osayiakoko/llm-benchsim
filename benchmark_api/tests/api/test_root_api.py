from fastapi.testclient import TestClient


def test_get_benchmark(client: TestClient):
    """
    Tests the GET / endpoint to retrieve benchmark data.

    Args:
        client (TestClient): The test client used to send the GET request.

    Returns:
        None
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["data"] == {"message": "Ok"}
    assert response.json()["success"] == True
