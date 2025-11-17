from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from .database import Base
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # "user" is the user who created this post
    user = relationship("User", back_populates="posts")

    # "votes" is a list of all Vote objects for this post
    votes = relationship("Votes", back_populates="post")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    # "posts" is a list of all Post objects created by this user
    posts = relationship("Post", back_populates="user")

    # "votes" is a list of all Vote objects by this user
    votes = relationship("Votes", back_populates="user")


class Votes(Base):
    __tablename__ = "votes"
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    post_id = Column(
        Integer,
        ForeignKey("posts.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )

    # "user" is the user object who made this vote
    user = relationship("User", back_populates="votes")

    # "post" is the post object that was voted on
    post = relationship("Post", back_populates="votes")
