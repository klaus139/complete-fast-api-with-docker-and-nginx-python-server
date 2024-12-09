from typing import Optional
from fastapi import Body, Response, status, HTTPException, Depends, FastAPI
from pydantic import BaseModel
from random import randrange
import psycopg 
import time
from psycopg.rows import dict_row
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)



app = FastAPI()


class Post(BaseModel):
    title: str
    content:str #4.50
    published: bool = True

# while True:
#     try:
#     # Update connection string format for psycopg3
#         conn = psycopg.connect("postgresql://postgres:klaus139@localhost/fastapi")
#         #cursor = conn.cursor()
#         cursor = conn.cursor(row_factory=dict_row)
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error", error)
#         time.sleep(2)

# try:
#     # Update connection string format for psycopg3
#     conn = psycopg.connect("postgresql://postgres:klaus139@localhost/fastapi")
#     cursor = conn.cursor()
#     print("Database connection was successful")
    
# except Exception as error:
#     print("Connecting to database failed")
#     print("Error", error)
#     time.sleep(2)


my_post = [{"title":"title of post 1", "content":"content of post 1", "id":1},{"title":"favorite food", "content":"i like pizza", "id":2}]

def findPost(id):
    for p in my_post:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i




# @app.get("/")
# async def read_root():
#     return {"Hello": "Welcome to my apiddddww"}

# @app.get("/squel-alchemy")
# def test_posts(db: Session = Depends(get_db)):
#     return {"status":"Success"}

# @app.get("/posts")
# def get_posts():
#     cursor.execute(""" SELECT * FROM posts """)
#     posts = cursor.fetchall()
#     print(posts)
#     return {
#         "data":posts
#     }

# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(post: Post):
#     cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
#     new_post = cursor.fetchone()
#     conn.commit() #to push the changes out and commit it to the database

#     return {
#         "data": new_post
#     }


# @app.get("/posts/{id}")
# def get_post(id: int):
#     cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (int(id),))  # Pass as a tuple
#     post = cursor.fetchone()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
   
#     return {
#         "post_detail": post 
#     }



# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id:int):
#     cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
#     deleted_post = cursor.fetchone()
#     conn.commit()
    
#     if deleted_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# @app.put("/posts/{id}")
# def update_post(id:int, post:Post):
#     cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s  RETURNING * """, (post.title, post.content, post.published, str(id)))
#     updated_post = cursor.fetchone()
#     conn.commit()

    
#     if updated_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
#     return { 
#         "data":updated_post
#     }