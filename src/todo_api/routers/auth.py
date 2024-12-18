from datetime import datetime, timedelta, timezone
from typing import Annotated, TypedDict

import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
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


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class DecodedTokenDict(TypedDict):
    username: str
    id: int
    role: str

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
    expiration_delta: timedelta = timedelta(minutes=settings.access_token_expire_minutes),
):
    encode: DecodedTokenDict = {"username": username, "id": user_id, "role": role}
    expires = datetime.now(timezone.utc) + expiration_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, settings.secret_key, settings.algorithm)


async def decode_access_token(token: Annotated[str, Depends(oauth2_bearer)]) -> DecodedTokenDict:
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

async def raise_if_no_valid_token(decoded_token: DecodedTokenDict):
    if decoded_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')

@router.post('/token', response_model=TokenResponse)
async def get_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_session):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
    token = create_access_token(user.username, user.id, user.role)
    return { 'access_token': token, 'token_type': 'bearer' }

