from typing import Optional, List
from fastapi import Body, Response, status, HTTPException, Depends, FastAPI
from pydantic import BaseModel
from random import randrange
import psycopg 
import time
from psycopg.rows import dict_row
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import post, user,auth





models.Base.metadata.create_all(bind=engine)



app = FastAPI()

    

while True:
    try:
    # Update connection string format for psycopg3
        conn = psycopg.connect("postgresql://postgres:klaus139@localhost/fastapi")
        #cursor = conn.cursor()
        cursor = conn.cursor(row_factory=dict_row)
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error", error)
        time.sleep(2)


my_post = [{"title":"title of post 1", "content":"content of post 1", "id":1},{"title":"favorite food", "content":"i like pizza", "id":2}]

def findPost(id):
    for p in my_post:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def read_root():
    return {"Hello": "Welcome to my apiddddww"}

