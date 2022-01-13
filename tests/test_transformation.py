from fastapi import FastAPI
from fastapi.testclient import TestClient

from oteapi.app.context import transformation
from oteapi.app.models.transformationconfig import TransformationStatus
from oteapi.app.strategy import loader

from .dummycache import DummyCache

app = FastAPI()

app.include_router(transformation.router, prefix="/transformation")
client = TestClient(app)

loader.load_plugins(["plugins.transformation_strategy.dummyplugin"])


async def override_depends_redis() -> DummyCache:
    return DummyCache(
        {
            "transformation-f752c613-fde0-4d43-a7f6-c50f68642daa": {
                "transformation_type": "script/dummy",
                "name": "script/dummy",
                "configuration": {},
            }
        }
    )


app.dependency_overrides[transformation.depends_redis] = override_depends_redis


def test_create_transformation():
    response = client.post(
        "/transformation/",
        json={
            "transformation_type": "script/dummy",
            "name": "script/dummy",
            "configuration": {},
        },
    )

    print("test_create_transformation response:", response.text)
    assert response.status_code == 200


def test_get_transformation():
    response = client.get(
        "/transformation/transformation-f752c613-fde0-4d43-a7f6-c50f68642daa"
    )
    print("test_get_transformation", response.text)
    assert response.status_code == 200


def test_initialize_transformation():
    response = client.post(
        "/transformation/transformation-f752c613-fde0-4d43-a7f6-c50f68642daa/execute",
        json={},
    )
    print("test_initialize_transformation response", response.text)
    assert response.status_code == 200


def test_get_transformation_status():
    response = client.get(
        "/transformation/transformation-f752c613-fde0-4d43-a7f6-c50f68642daa/status?task_id="
    )
    tr = TransformationStatus(**response.json())
    print(response.json())
    print("test_get_transformation_status response:", response.text)
    assert response.status_code == 200


def test_execute_transformation():
    response = client.post(
        "/transformation/transformation-f752c613-fde0-4d43-a7f6-c50f68642daa/execute",
        json={},
    )
    print("test_execute_transformation response:", response.text)
    assert response.status_code == 200
