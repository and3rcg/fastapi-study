from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app # Import the main app
from users.routes import get_db # Import the original dependency
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


def test_create_user():
    response = client.post(
        "/users",
        json={"username": "testuser", "email": "test@yopmail.com", "password": "test123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@yopmail.com"
    assert "id" in data
