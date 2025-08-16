from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from main import app # Import the main app
from items.routes import get_db # Import the original dependency
import models

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def setup_function():
    models.Base.metadata.create_all(bind=engine)

def teardown_function():
    models.Base.metadata.drop_all(bind=engine)

def test_create_item():
    response = client.post(
        "/items/",
        json={"name": "Test Item", "price": 10.5, "description": "An item for testing"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["price"] == 10.5
    assert "id" in data

def test_get_single_item():
    create_response = client.post(
        "/items/",
        json={"name": "Another Item", "price": 99.99},
    )
    assert create_response.status_code == 200
    item_id = create_response.json()["id"]

    get_response = client.get(f"/items/{item_id}")

    assert get_response.status_code == 200
    data = get_response.json()
    assert data["name"] == "Another Item"
    assert data["id"] == item_id

def test_get_nonexistent_item():
    response = client.get("/items/99999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}
