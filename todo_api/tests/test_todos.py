from .db_config import override_get_db_session, override_decode_access_token, app, client
from ..routers.users import get_db_session, decode_access_token
from fastapi import status

app.dependency_overrides[get_db_session] = override_get_db_session
app.dependency_overrides[decode_access_token] = override_decode_access_token

def test_get_todos(test_todo):
  response = client.get('/todo')
  assert response.status_code == status.HTTP_200_OK
  jsonResponse = response.json()
  responseTodo = jsonResponse[0]
  assert responseTodo.get('id') == test_todo.id
  assert responseTodo.get('title') == test_todo.title
  assert responseTodo.get('description') == test_todo.description
  assert responseTodo.get('user_id') == test_todo.user_id
 

def test_get_a_todo(test_todo):
  response = client.get('/todo/1')
  assert response.status_code == status.HTTP_200_OK
  responseTodo = response.json()
  assert responseTodo.get('id') == test_todo.id
  assert responseTodo.get('title') == test_todo.title
  assert responseTodo.get('description') == test_todo.description
  assert responseTodo.get('user_id') == test_todo.user_id

def test_get_a_unexistent_todo(test_todo):
  response = client.get('/todo/9999')
  assert response.status_code == status.HTTP_404_NOT_FOUND
  assert response.json() == { 'detail': 'Todo not found.' }

def test_create_todo(test_user):
  body = {
    "title": "new todo",
    "description": "test new todo",
    "complete": False
  }
  response = client.post('/todo', json=body)
  assert response.status_code == status.HTTP_201_CREATED

def test_create_todo_without_description(test_user):
  body = {
    "title": "new todo",
    "complete": False
  }
  response = client.post('/todo', json=body)
  assert response.status_code == status.HTTP_201_CREATED

def test_create_todo_without_complete(test_user):
  body = {
    "title": "new todo",
  }
  response = client.post('/todo', json=body)
  assert response.status_code == status.HTTP_201_CREATED

def test_update_todo(test_user, test_todo):
  body = {
    "title": "new title",
  }
  response = client.patch('/todo/1', json=body)
  assert response.status_code == status.HTTP_204_NO_CONTENT

def test_update_unexistent_todo(test_user, test_todo):
  body = {
    "title": "new title",
  }
  response = client.patch('/todo/999', json=body)
  assert response.status_code == status.HTTP_404_NOT_FOUND
  assert response.json() == { 'detail': 'Todo not found.' }

def test_delete_todo(test_user, test_todo):
  response = client.delete('/todo/1')
  assert response.status_code == status.HTTP_200_OK

def test_delete_unexistent_todo(test_user, test_todo):
  response = client.delete('/todo/999')
  assert response.status_code == status.HTTP_404_NOT_FOUND
  assert response.json() == { 'detail': 'Todo not found.' }
