from app import schemas
from .database import client, session


def test_root(client):
    res = client.get("/")
    json = res.json()
    msg = json.get("message")
    assert msg == "Hello World"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "qwerty@gmail.com", "password": "qwerty"}
    )
    new_user = schemas.UserOut(**res.json())

    assert new_user.email == "qwerty@gmail.com"
    assert res.status_code == 201


def test_login_user(client):

    client.post("/users/", json={"email": "qwerty@gmail.com", "password": "qwerty"})

    res = client.post(
        "/login", data={"username": "qwerty@gmail.com", "password": "qwerty"}
    )

    assert res.status_code == 200
