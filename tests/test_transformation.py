from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.context import transformation
from .dummycache import DummyCache

app = FastAPI()

app.include_router(transformation.router, prefix='/trans')
client = TestClient(app)

async def override_depends_redis() -> DummyCache:
    return DummyCache({'101':{'transformation_type':'script/dummy'}})

app.dependency_overrides[transformation.depends_redis] = override_depends_redis

def test_create_transformation():
    response = client.post(
        "/trans/",
        json= {"transformation_type": "script/dummy"})

    print ('test_create_transformation response:', response.text)
    assert response.status_code == 200

def test_get_transformation_status():
    response = client.get(
        "/trans/101/status/"
    )
    print ('test_get_transformation_status response:', response.text)
    #assert response.status_code == 200