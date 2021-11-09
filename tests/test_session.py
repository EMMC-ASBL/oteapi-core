from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.context import session
from .dummycache import DummyCache

app = FastAPI()

app.include_router(session.router, prefix="/session")
client = TestClient(app)


async def override_depends_redis() -> DummyCache:
    return DummyCache({"1": {"foo": "bar"}, "2": {"foo": "bar"}})


app.dependency_overrides[session.depends_redis] = override_depends_redis


def test_list_session():
    response = client.get("/session")
    print("output", response.text)
    assert response.json() == {"keys": ["1", "2"]}
    assert response.status_code == 200


def test_create_session():
    response = client.post(
        "/session/",
        headers={"accept": "application/json", "Content-Type": "application/json"},
        json={"foo": "bar"},
    )
    # Ensure that session returns with a session id
    assert "session_id" in response.json()
    assert response.status_code == 200
