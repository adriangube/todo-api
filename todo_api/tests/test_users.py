from .db_config import override_get_db_session, override_decode_access_token, app, client
from ..routers.users import get_db_session, decode_access_token
from fastapi import status

app.dependency_overrides[get_db_session] = override_get_db_session
app.dependency_overrides[decode_access_token] = override_decode_access_token


def test_get_users(test_current_users):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK

    jsonResponse = response.json()
    assert jsonResponse.get('id') == 1
    assert jsonResponse.get("username") == test_current_users.username
    assert jsonResponse.get("email") == test_current_users.email
    assert jsonResponse.get('role')  == test_current_users.role

def test_create_user():
    response = client.post('/user', json={"username": "test1", "email": "test@test.com", "password": "test123456", "role": "user"})
    assert response.status_code == status.HTTP_201_CREATED