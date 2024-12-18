from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session, load_only
from starlette import status

from .auth import hash_password

from ..database import get_db_session
from ..models import Users

router = APIRouter(prefix="/user", tags=["user"])

db_session = Annotated[Session, Depends(get_db_session)]


class CreateUserRequest(BaseModel):
    username: str = Field(min_length=5)
    email: str = EmailStr
    password: str = Field(min_length=10)
    role: str = Field(default='user')

def getUserSelectableFields():
    selected_fields = ['id', 'username', 'email', 'role']
    fields = [getattr(Users, f) for f in selected_fields]
    return fields


@router.get("/", status_code=status.HTTP_200_OK)
async def get_users(db: db_session):
    fields = getUserSelectableFields()
    return db.query(Users).options(load_only(*fields)).all()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_session, create_user_request: CreateUserRequest):
    new_user = Users(
        username=create_user_request.username,
        email=create_user_request.email,
        hashed_password=hash_password(create_user_request.password),
        role=create_user_request.role
    )

    db.add(new_user)
    db.commit()
