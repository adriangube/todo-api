from .db_config import override_get_db_session, override_decode_access_token, app, client
from ..routers.users import get_db_session, decode_access_token
from fastapi import status

app.dependency_overrides[get_db_session] = override_get_db_session
app.dependency_overrides[decode_access_token] = override_decode_access_token


def test_get_users_success(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK

    jsonResponse = response.json()
    assert jsonResponse.get('id') == 1
    assert jsonResponse.get("username") == test_user.username
    assert jsonResponse.get("email") == test_user.email
    assert jsonResponse.get('role')  == test_user.role

def test_create_user_success():
    body = {
        "username": "test1",
        "email": "test@test.com",
        "password": "test123456",
    }
    response = client.post('/user', json=body)
    assert response.status_code == status.HTTP_201_CREATED

def test_create_user_short_password():
    body = {
        "username": "test1",
        "email": "test@test.com",
        "password": "short",
    }
    response = client.post('/user', json=body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_create_user_short_username():
    body = {
        "username": "a",
        "email": "test",
        "password": "test123456",
    }
    response = client.post('/user', json=body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_update_password_success(test_user):
    body = {
        "password": "password123456",
        "new_password": "newpassword123456"
    }
    response = client.put('/user/password', json=body)
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_update_password_invalid_current_password(test_user):
    body = {
        "password": "wrong_password",
        "new_password": "newpassword123456"
    }
    response = client.put('/user/password', json=body)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == { 'detail': 'The password provided doesn´t match the current password.' }

def test_update_password_short_password_error(test_user):
    body = {
        "password": "password123456",
        "new_password": "short"
    }
    response = client.put('/user/password', json=body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
