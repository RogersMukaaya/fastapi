from app import schemas
import pytest
from jose import jwt
from app.config import settings



def test_create_user(client, session):
  response = client.post(
    "/users/",
    json={
      "email": "test345@gmail.com",
      "password": "45454password123",
      "phone_number": "454541234567890"
    }
  )

  new_user = schemas.UserOut(**response.json())
  assert new_user.email == "test345@gmail.com"
  assert response.status_code == 201

def test_login_user(test_user, client):
  response = client.post(
    "/login",
    data={
      "username": test_user['email'],
      "password": test_user['password']
    }
  )
  login_res = schemas.Token(**response.json())
  payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
  id: str = payload.get("user_id")
  assert id == str(test_user['id'])
  assert login_res.token_type == "bearer"
  assert response.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
  ("tester@gmail.com", "wrongpassword", 403),
  ("tester@gmail.com", "wrongpasswordere", 403)
])
def test_incorrect_login_user(test_user, client, email, password, status_code):
  response = client.post(
    "/login",
    data={
      "username": email,
      "password": password
    }
  )
  assert response.status_code == status_code
  assert response.json().get('detail') == "Invalid Credentials"