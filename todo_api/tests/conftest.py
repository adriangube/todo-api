import pytest

from ..models import Users
from .db_config import TestDatabaseSession, engine
from ..routers.auth import pwd_context

@pytest.fixture
def test_user():
  user = Users(
    id=1,
    username='testUser',
    email='test@email.com',
    hashed_password=pwd_context.hash('password123456'),
    is_active=True,
    role = 'admin'
  )
  db = TestDatabaseSession
  db.add(user)
  db.commit()
  yield user


@pytest.fixture(scope="function", autouse=True)
def clean_db():
    connection = engine.connect()
    transaction = connection.begin()
    TestDatabaseSession.bind = connection

    yield
    transaction.rollback()
    connection.close()