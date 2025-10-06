from fastapi import FastAPI, Response, status, HTTPException, APIRouter
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from fastapi import Depends
from ..database import get_db
from typing import List
from .. import oauth2
from typing import Optional
from sqlalchemy import func

router = APIRouter(
  prefix="/posts",
  tags=['Posts']
)

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favorite foods", "content": "I like pizza", "id": 2}]

# @router.get("/")
# def root():
#   return {"message": "Hello World"}

@router.get("/", response_model=List[schemas.PostOut])
def test_post(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
  # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all()

  results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).all()

  return results

# @router.get("/posts")
# def get_posts():
#   cursor.execute(""" SELECT * FROM posts """)
#   posts = cursor.fetchall()
#   return posts

# @router.post("/posts", status_code=status.HTTP_201_CREATED)
# def get_posts(post: Post):
#   cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
#   new_post = cursor.fetchone()

#   conn.commit()
#   return {"data": new_post}


@router.post("/")
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), response_model=schemas.Post, user_id: int = Depends(oauth2.get_current_user)):
  new_post = models.Post(**post.dict(), owner_id=int(user_id.id))
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return new_post


# def find_post(id):
#   print(my_posts)
#   for p in my_posts:
#     if p['id'] == id:
#       return p



# @router.get("/posts/{id}")
# def get_post(id: int, response: Response):
#   cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
#   post = cursor.fetchone()
#   if not post:
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
#   return {"post_detail": post}


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
  # post = db.query(models.Post).filter(models.Post.id == id).first()

  post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
  return post





# @router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#   cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
#   deleted_post = cursor.fetchone()
#   if deleted_post == None:
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
#   conn.commit()
#   return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
  post = db.query(models.Post).filter(models.Post.id == id)
  if post.first() == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
  
  if post.first().owner_id != user_id.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
  
  post.delete(synchronize_session=False)
  db.commit()
  return Response(status_code=status.HTTP_204_NO_CONTENT)





# @router.put("/posts/{id}")
# def update_post(id: int, post: Post):
#   cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
#   updated_post = cursor.fetchone()

#   if updated_post == None:
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
  
#   conn.commit()
#   return {"data": updated_post}

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
  post_query = db.query(models.Post).filter(models.Post.id == id)
  updated_post = post_query.first()

  if updated_post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
  
  if updated_post.owner_id != user_id.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
  
  post_query.update(post.model_dump(), synchronize_session=False)
  db.commit()
  return post_query.first()