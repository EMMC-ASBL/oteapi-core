from fastapi.testclient import TestClient
from app import create_app

app = create_app()
client = TestClient(app)

def test_read_home():
    response = client.get("/api/v1/test")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
