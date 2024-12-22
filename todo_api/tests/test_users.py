from .config import *
from ..routers.users import get_db_session, decode_access_token
from fastapi import status
from .fixtures.fixtures_users import test_users  # noqa: F401

app.dependency_overrides[get_db_session] = override_get_db_session
app.dependency_overrides[decode_access_token] = override_decode_access_token


def test_return_user(test_users):  # noqa: F811
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
