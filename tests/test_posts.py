from typing import List
from app import schemas
import pytest


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)

    post_map = map(validate, res.json())
    post_list = list(post_map)  # Convert to list ONCE

    print(post_list)  # Print the list
    # Now you can use post_list for assertions if you want

    assert len(res.json()) == len(test_posts)

    assert res.status_code == 200


def test_uauthorized_user_get_all_posts(client, test_posts):
    res = client.get(f"/posts/")
    assert res.status_code == 401


def test_uauthorized_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_which_does_not_exists(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/11111")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 200
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title


@pytest.mark.parametrize(
    "title, content, published",
    [
        ("awesome new title", "some new type of content", True),
        ("fav pizza", "hot pizza", False),
        ("tallest building", "wahoo", True),
    ],
)
def test_create_post(
    authorized_client, test_user, test_posts, title, content, published
):
    res = authorized_client.post(
        "/posts/", json={"title": title, "content": content, "published": published}
    )

    created_post = schemas.PostOut(**res.json())
    assert res.status_code == 201
    assert created_post.Post.title == title
    assert created_post.Post.content == content
    assert created_post.Post.published == published
    assert created_post.Post.user_id == test_user["id"]
