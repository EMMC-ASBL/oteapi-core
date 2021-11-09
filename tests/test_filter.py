from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.context import datafilter

from .dummycache import DummyCache

app = FastAPI()

app.include_router(datafilter.router, prefix="/filter")
client = TestClient(app)


async def override_depends_redis() -> DummyCache:
    return DummyCache()


app.dependency_overrides[datafilter.depends_redis] = override_depends_redis


def test_create_filter():
    response = client.post(
        "/filter/",
        json={
            "filterType": "filter/demo",
            "query": "SELECT * FROM Test",
            "condition": "",
            "limit": 1,
            "configuration": {},
        },
    )
    # Ensure that session returns with a session id
    assert "filter_id" in response.json()
    assert response.status_code == 200
