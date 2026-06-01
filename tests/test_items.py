import pytest
from fastapi.testclient import TestClient
from app.app.main import app

client = TestClient(app)

def test_create_item():
    response = client.post("/items/", json={"name": "Test", "price": 100})
    assert response.status_code == 200