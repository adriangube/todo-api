from ..settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from ..database import Base
from ..routers.auth import DecodedTokenDict
from fastapi.testclient import TestClient
from ..main import app

engine = create_engine(settings.test_database_url)

TestDatabaseSession = Session(bind=engine, autocommit=False, autoflush=False)

def override_get_db_session():
  db_session = TestDatabaseSession
  try:
    yield db_session
  finally:
    db_session.close()

Base.metadata.create_all(bind=engine)

def override_decode_access_token() -> DecodedTokenDict:
  return { 'id': 1, 'role': 'admin', 'username': 'testUser'}

client = TestClient(app)