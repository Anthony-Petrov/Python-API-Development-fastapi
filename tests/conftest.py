from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from app.database import get_db
from app.main import app
from app import models, schemas
from app.config import settings
from sqlalchemy.orm import sessionmaker
from app.oauth2 import create_access_token
from app import models
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}_test"

if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace(
        "postgres://", "postgresql://", 1
    )

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db(scope="module"):
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def session():
    models.Base.metadata.drop_all(bind=engine)  # type: ignore
    models.Base.metadata.create_all(bind=engine)  # type: ignore
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "qwerty@gmail.com", "password": "qwerty"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()

    new_user["password"] = user_data["password"]

    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def test_posts(test_user, session):
    posts_data = [
        {"title": "1st title", "content": "1st content", "user_id": test_user["id"]},
        {"title": "2nd title", "content": "2nd content", "user_id": test_user["id"]},
        {"title": "3rd title", "content": "3rd content", "user_id": test_user["id"]},
    ]

    # Convert the list of dicts -> list of Models automatically
    # The ** unpacking does the work for you
    posts_map = map(lambda post: models.Post(**post), posts_data)
    posts = list(posts_map)

    session.add_all(posts)
    session.commit()

    # Verify they were saved
    posts = session.query(models.Post).all()

    # CRITICAL: Return them so the test can use them
    return posts
