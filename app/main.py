from fastapi import FastAPI
from random import randrange
from . import models
from .database import engine, get_db
from .routers import posts, users, auth, votes
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)  # type: ignore

app = FastAPI()

origins = ["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Hello World"}


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)
