from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from app.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db
from app.config import settings
from app.database import Base
import pytest
from app.oauth2 import create_access_token
from app import models

SQLALCHEMY_DATABASE_URL = (
  f'postgresql://{settings.database_username}:{settings.database_password}'
  f'@{settings.database_host}:{settings.database_port}/{settings.database_name}_test'
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def session():
  Base.metadata.drop_all(bind=engine)
  Base.metadata.create_all(bind=engine)
  db = TestingSessionLocal()
  try:
    yield db
  finally:
    db.close()

@pytest.fixture(scope="function")
def client(session):

  def override_get_db():
    try:
      yield session
    finally:
      session.close()

  app.dependency_overrides[get_db] = override_get_db

  yield TestClient(app)

@pytest.fixture
def test_user(client):
  user_date = {
    "email": "test345@gmail.com",
    "password": "45454password123",
    "phone_number": "454541234567890"
  }
  res = client.post("/users/", json=user_date)
  print(res.json())
  assert res.status_code == 201
  new_user = res.json()
  new_user['password'] = user_date['password']
  return new_user

@pytest.fixture
def test_user2(client):
  user_date = {
    "email": "test34534@gmail.com",
    "password": "45434354password123",
    "phone_number": "434354541234567890"
  }
  res = client.post("/users/", json=user_date)
  print(res.json())
  assert res.status_code == 201
  new_user = res.json()
  new_user['password'] = user_date['password']
  return new_user

@pytest.fixture
def token(test_user):
  create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
  client.headers = {
    **client.headers,
    "Authorization": f"Bearer {token}"
  }
  return client
 
@pytest.fixture
def test_posts(test_user, test_user2, session):
  posts_data = [
    {
      "title": "first title",
      "content": "first content",
      "owner_id": test_user['id']
    },
    {
      "title": "second title",
      "content": "second content",
      "owner_id": test_user['id']
    },
    {
      "title": "third title",
      "content": "third content",
      "owner_id": test_user['id']
    },
    {
      "title": "third title",
      "content": "third content",
      "owner_id": test_user2['id']
    }
  ]

  def create_post_model(post):
    return models.Post(**post)

  post_map = map(create_post_model, posts_data)
  posts = list(post_map)

  session.add_all(posts)
  session.commit()
  posts = session.query(models.Post).all()
  return posts
