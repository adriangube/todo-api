from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from starlette import status

from ..models import Todos

from .auth import DecodedTokenDict, decode_access_token, raise_if_no_valid_token
from ..database import get_db_session
from pydantic import BaseModel, Field

router = APIRouter(prefix="/todo", tags=["todo"])

db_session = Annotated[Session, Depends(get_db_session)]
decoded_access_token = Annotated[DecodedTokenDict, Depends(decode_access_token)]


class TodosResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    complete: bool
    user_id: int


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: Optional[str] = Field(default=None)
    complete: Optional[bool] = Field(default=False)

class PartialUpdate(BaseModel):
    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    complete: Optional[bool] = Field(default=None)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[TodosResponse])
async def read_all(decoded_token: decoded_access_token, db: db_session):
    await raise_if_no_valid_token(decoded_token)
    return db.query(Todos).filter(Todos.user_id == decoded_token.get("id")).all()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(
    decoded_token: decoded_access_token,
    db: db_session,
    create_todo_request: TodoRequest,
):
    await raise_if_no_valid_token(decoded_token)
    new_todo = Todos()
    new_todo.title = create_todo_request.title
    new_todo.description = create_todo_request.description
    new_todo.complete = create_todo_request.complete
    new_todo.user_id = decoded_token.get("id")
    db.add(new_todo)
    db.commit()


@router.patch("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    decoded_token: decoded_access_token,
    db: db_session,
    update_todo_request: PartialUpdate,
    todo_id: int = Path(gt=0),
):
    await raise_if_no_valid_token(decoded_token)
    todo = (
        db.query(Todos)
        .filter(Todos.id == todo_id, Todos.user_id == decoded_token.get("id"))
        .first()
    )
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found."
        )
    update_fields = { key: value for key, value in update_todo_request.model_dump(exclude_unset=True).items() }
    for key, value in update_fields.items():
        setattr(todo, key, value)
    
    db.add(todo)
    db.commit()