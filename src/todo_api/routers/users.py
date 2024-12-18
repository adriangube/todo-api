from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field, model_validator
from sqlalchemy.orm import Session, load_only
from starlette import status

from .auth import (
    DecodedTokenDict,
    raise_if_no_valid_token,
    decode_access_token,
    hash_password,
    verify_password,
)

from ..database import get_db_session
from ..models import Users

router = APIRouter(prefix="/user", tags=["user"])

db_session = Annotated[Session, Depends(get_db_session)]
decoded_access_token = Annotated[DecodedTokenDict, Depends(decode_access_token)]


class CreateUserRequest(BaseModel):
    username: str = Field(min_length=5)
    email: str = EmailStr
    password: str = Field(min_length=10)
    role: str = Field(default="user")


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str

class UserVerification(BaseModel):
    password: str = Field(min_length=10)
    new_password: str = Field(min_length=10)

    @model_validator(mode='after')
    def check_passwords(self):
        if self.password == self.new_password:
            raise ValueError('The new_password must be different from the current password.')
        return self


def getUserSelectableFields():
    selected_fields = ["id", "username", "email", "role"]
    fields = [getattr(Users, f) for f in selected_fields]
    return fields


@router.get("/", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_users(decoded_token: decoded_access_token, db: db_session):
    raise_if_no_valid_token(decoded_token)
    fields = getUserSelectableFields()
    return (
        db.query(Users)
        .options(load_only(*fields))
        .filter(Users.id == decoded_token.get("id"))
        .first()
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_session, create_user_request: CreateUserRequest):
    new_user = Users(
        username=create_user_request.username,
        email=create_user_request.email,
        hashed_password=hash_password(create_user_request.password),
        role=create_user_request.role,
    )

    db.add(new_user)
    db.commit()

@router.put('/password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    decoded_token: decoded_access_token,
    db: db_session,
    user_verification: UserVerification
):
    raise_if_no_valid_token(decoded_token)
    user_model = db.query(Users).filter(Users.id == decoded_token.get('id')).first()
    if not verify_password(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='The password provided doesn´t match the current password.')
    
    user_model.hashed_password = hash_password(user_verification.new_password)

    db.add(user_model)
    db.commit()

