from typing import Annotated, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from ..models import Todos

from .auth import DecodedTokenDict, decode_access_token, raise_if_no_valid_token
from ..database import get_db_session
from pydantic import BaseModel, Field

router = APIRouter(prefix="/todo", tags=["todo"])

db_session = Annotated[Session, Depends(get_db_session)]
decoded_access_token = Annotated[DecodedTokenDict, Depends(decode_access_token)]

class CreateTodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: Optional[str] = Field(default=None)
    complete: Optional[bool] = Field(default=False)


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(decoded_token: decoded_access_token, db: db_session):
    await raise_if_no_valid_token(decoded_token)
    return db.query(Todos).filter(Todos.user_id == decoded_token.get("id")).all()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_todo(decoded_token: decoded_access_token, db: db_session, create_todo_request: CreateTodoRequest):
    await raise_if_no_valid_token(decoded_token)
    new_todo = Todos()
    new_todo.title = create_todo_request.title
    new_todo.description = create_todo_request.description
    new_todo.complete = create_todo_request.complete
    new_todo.user_id = decoded_token.get('id')
    db.add(new_todo)
    db.commit()

