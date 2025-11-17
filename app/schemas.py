from typing import Optional
from httpx import post
from pydantic import BaseModel, conint
from datetime import datetime
from pydantic import EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        # orm_mode = True
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserOut

    class Config:
        # orm_mode = True
        from_attributes = True


class Vote(BaseModel):
    post_id: int
    direction_vote: int


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        # orm_mode = True
        from_attributes = True
