import pytest
from fastapi.testclient import TestClient


def test_read_items(client: TestClient) -> None:
    response = client.get("")
    assert response.status_code == 200
    assert response.json() == {"ping": "PONG"}
