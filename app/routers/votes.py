from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import engine, get_db

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
):

    post = db.query(models.Post).filter(vote.post_id == models.Post.id).first()  # type: ignore

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote.post_id} does not exist!",
        )

    vote_query = db.query(models.Votes).filter(
        current_user.id == models.Votes.user_id,
        vote.post_id == models.Votes.post_id,
    )  # type: ignore

    found_vote = vote_query.first()
    if vote.direction_vote == 1:
        if found_vote is None:
            new_vote = models.Votes(user_id=current_user.id, post_id=vote.post_id)  # type: ignore
            db.add(new_vote)
            db.commit()
            return {
                "Vote has been sent": f"User with id {current_user.id} has liked post with id {vote.post_id}."
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Vote already counted!"
            )

    elif vote.direction_vote == 0:
        if found_vote:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No vote exists!"
            )
