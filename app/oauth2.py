from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, status, HTTPException
from app import schemas
from fastapi.security import OAuth2PasswordBearer
from . import schemas, database
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import database, schemas, models, utils, oauth2
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# SECRET_KEY
# Algorithm
# Expiration time

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get("user_id")  # type: ignore

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token, credentials_exception)  # type: ignore

    user = db.query(models.User).filter(models.User.id == token.id).first()  # type: ignore

    return user
