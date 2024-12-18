from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from ..models import Todos

from .auth import DecodedTokenDict, decode_access_token, raise_if_no_valid_token
from ..database import get_db_session

router = APIRouter(prefix="/todo", tags=["todo"])

db_session = Annotated[Session, Depends(get_db_session)]
decoded_access_token = Annotated[DecodedTokenDict, Depends(decode_access_token)]


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(decoded_token: decoded_access_token, db: db_session):
    raise_if_no_valid_token(decoded_token)
    return db.query(Todos).filter(Todos.user_id == decoded_token.get("id")).all()
