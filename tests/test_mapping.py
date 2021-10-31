from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.context import mapping
from .dummycache import DummyCache
from app.strategy import loader

app = FastAPI()

app.include_router(mapping.router, prefix='/mapping')
client = TestClient(app)

loader.load_plugins(['plugins.mapping-strategy.demo-mapping'])


async def override_depends_redis() -> DummyCache:
    return DummyCache(
        {"mapping-a2d6b3d5-9b6b-48a3-8756-ae6d4fd6b81e":
            {
            "mappingType": "mapping/demo",
            "prefixes": {
                ":": "<http://namespace.example.com/ns#"
            },
            "triples": [
                [":a", ":has", ":b"]
            ],
            "configuration": {}
            }
        })


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


def test_get_mapping():
    response = client.get('/mapping/mapping-a2d6b3d5-9b6b-48a3-8756-ae6d4fd6b81e')
    print ('test_get_mapping response', response.text)
    assert(response.status_code == 200)


def test_initialize_mapping():
    response = client.post(
        '/mapping/mapping-a2d6b3d5-9b6b-48a3-8756-ae6d4fd6b81e/initialize',
        json = {}
        )
    print ('test_initialize_mapping response',response.text)
    assert(response.status_code == 200)