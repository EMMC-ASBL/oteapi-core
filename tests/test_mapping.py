from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.context import mapping
from .dummycache import DummyCache

app = FastAPI()

app.include_router(mapping.router, prefix='/mapping')
client = TestClient(app)

async def override_depends_redis() -> DummyCache:
    return DummyCache()

app.dependency_overrides[mapping.depends_redis] = override_depends_redis

def test_create_mapping():
    response = client.post(
        "/mapping/",
        json={
            "mappingType": "mapping/demo",
            "prefixes": {},
            "triples": [ ["a", "b", "c"] ],
            "configuration": { }
        })
    assert "mapping_id" in response.json()
    assert response.status_code == 200
