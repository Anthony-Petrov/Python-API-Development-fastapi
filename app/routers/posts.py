from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import engine, get_db
from sqlalchemy import func

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    # posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all() # type: ignore

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()  # type: ignore

    posts = (
        (
            db.query(models.Post, func.count(models.Votes.post_id).label("votes"))
            .join(models.Votes, models.Post.id == models.Votes.post_id, isouter=True)  # type: ignore
            .group_by(models.Post.id)
        )
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )

    return posts


@router.get("/{id}", response_model=schemas.PostOut)
def get_post_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
):

    # post = db.query(models.Post).filter(models.Post.id == id).first()  # type: ignore
    post = (
        (
            db.query(models.Post, func.count(models.Votes.post_id).label("votes"))
            .join(models.Votes, models.Post.id == models.Votes.post_id, isouter=True)  # type: ignore
            .group_by(models.Post.id)
        )
        .filter(id == models.Post.id)
        .first()
    )

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
):

    new_post = models.Post(user_id=current_user.id, **post.model_dump())  # type: ignore

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"Post": new_post, "votes": 0}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):

    post_query = db.query(models.Post).filter(models.Post.id == id)  # type: ignore
    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist",
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    "/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.PostOut
)
def update_post(
    id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
):

    post_q = db.query(models.Post).filter(models.Post.id == id)  # type: ignore
    post = post_q.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist",
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    post_q.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    post = (
        db.query(models.Post, func.count(models.Post.id).label("votes"))
        .join(models.Votes, models.Post.id == models.Votes.post_id, isouter=True)  # type: ignore
        .group_by(models.Post.id)
        .filter(id == models.Post.id)
    ).first()

    return post
