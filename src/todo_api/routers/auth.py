from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from ..database import get_db_session
from ..models import Users
from ..settings import settings

router = APIRouter(prefix="/auth", tags=["auth"])

db_session = Annotated[Session, Depends(get_db_session)]


class Token(BaseModel):
    access_token: str
    token_type: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(plain_password: str):
    return pwd_context.hash(plain_password)


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not verify_password(
        plain_password=password, hashed_password=user.hashed_password
    ):
        return False
    return user


def create_access_token(
    username: str,
    user_id: int,
    role: str,
    expiration_delta: timedelta = settings.access_token_expire_minutes,
):
    encode = {"username": username, "id": user_id, "role": role}
    expires = datetime.now(timezone.utc) + expiration_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, settings.secret_key, settings.algorithm)


async def decode_access_token(token: Annotated[str, Depends(oauth2_bearer)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        username: str = payload.get("username")
        user_id: str = payload.get("id")
        role: str = payload.get("role")
        if username is None or user_id is None or role is None:
            raise credentials_exception
        return {"username": username, "id": user_id, "role": role}
    except InvalidTokenError:
        raise credentials_exception

