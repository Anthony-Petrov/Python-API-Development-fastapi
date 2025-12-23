import pytest
from jose import jwt
from app import schemas

from app.config import settings


# def test_root(client):
#     res = client.get("/")
#     json = res.json()
#     msg = json.get("message")
#     assert msg == "Hello World"
#     assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "qwerty@gmail.com", "password": "qwerty"}
    )
    new_user = schemas.UserOut(**res.json())

    assert new_user.email == "qwerty@gmail.com"
    assert res.status_code == 201


def test_login_user(client, test_user):

    res = client.post(
        "/login",
        data={
            "username": test_user["email"],  # Use data from fixture
            "password": test_user["password"],  # Use data from fixture
        },
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(
        login_res.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    id: int = payload.get("user_id")  # type: ignore
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "qwerty", 403),
        ("qwerty@gmail.com", "wrongpassword", 403),
        ("wrongemail@gmail.com", "wrongpassword", 403),
        (None, "qwerty", 403),
        ("qwerty@gmail.com", None, 403),
    ],
)
def test_incorrect_login(client, test_user, email, password, status_code):

    res = client.post(
        "/login",
        data={
            "username": email,
            "password": password,
        },
    )
    assert res.status_code == status_code
