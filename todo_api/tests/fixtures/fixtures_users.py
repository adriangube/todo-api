import pytest
from sqlalchemy import text

from ...models import Users
from ..config import TestDatabaseSession, engine

@pytest.fixture
def test_users():
  user = Users(
    id=1,
    username='testUser',
    email='test@email.com',
    hashed_password='123456',
    is_active=True,
    role = 'admin'
  )
  db = TestDatabaseSession
  db.add(user)
  db.commit()
  yield user
  with engine.connect() as connection:
    connection.execute(text('DELETE FROM users;'))
    connection.commit()
