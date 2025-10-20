def test_vote_on_post(authorized_client, test_posts):
  res = authorized_client.post(
    "/vote/",
    json={
      "post_id": test_posts[0].id,
      "dir": 1
    }
  )
  assert res.status_code == 201

def test_vote_on_post_twice(authorized_client, test_posts):
  authorized_client.post(
    "/vote/",
    json={
      "post_id": test_posts[0].id,
      "dir": 1
    }
  )
  res = authorized_client.post(
    "/vote/",
    json={
      "post_id": test_posts[0].id,
      "dir": 1
    }
  )
  assert res.status_code == 409

def test_remove_vote(authorized_client, test_posts):
  authorized_client.post(
    "/vote/",
    json={
      "post_id": test_posts[0].id,
      "dir": 1
    }
  )
  res = authorized_client.post(
    "/vote/",
    json={
      "post_id": test_posts[0].id,
      "dir": 0
    }
  )
  assert res.status_code == 201

def test_remove_vote_nonexistent(authorized_client, test_posts):
  res = authorized_client.post(
    "/vote/",
    json={
      "post_id": test_posts[0].id,
      "dir": 0
    }
  )
  assert res.status_code == 404