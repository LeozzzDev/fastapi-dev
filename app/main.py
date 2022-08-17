from random import randrange
from re import S
from sqlite3 import Cursor
from typing import Optional
from venv import create
from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

posts = []

def get_post_by_id(id):
    for post in posts:
        if post['id'] == id:
            return post

def get_index_by_post_id(id):
    for i, post in enumerate(posts):
        if post['id'] == id:
            return i

@app.get("/posts")
async def get_posts():

    with psycopg2.connect(host="localhost", database="social", user="leo", 
    password="psw", cursor_factory=RealDictCursor) as postgres_connection:
        
        postgres_connection.autocommit = True
        with postgres_connection.cursor() as cursor:

            cursor.execute("SELECT * FROM posts")
            db_posts = cursor.fetchall()
            return {"data": db_posts}

@app.get("/posts/{id}")
async def get_post(id: int):

    with psycopg2.connect(host="localhost", database="social", user="leo", 
    password="psw", cursor_factory=RealDictCursor) as postgres_connection:
        
        postgres_connection.autocommit = True
        with postgres_connection.cursor() as cursor:
            
            cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id)))
            post = cursor.fetchone()

            if not post:
                raise HTTPException(status_code=404, detail=f"post with id:{id} not found")
            return post


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):

    with psycopg2.connect(host="localhost", database="social", user="leo", 
    password="psw", cursor_factory=RealDictCursor) as postgres_connection:

        postgres_connection.autocommit = True
        with postgres_connection.cursor() as cursor:

            cursor.execute("""INSERT INTO posts (title, content, published)
            VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
            
            created_post = cursor.fetchone()
            postgres_connection.commit()
            return created_post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):

    with psycopg2.connect(host="localhost", database="social", user="leo", 
    password="psw", cursor_factory=RealDictCursor) as postgres_connection:

        postgres_connection.autocommit = True
        with postgres_connection.cursor() as cursor:

            cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id)))
            deleted_post = cursor.fetchone()

            if not deleted_post:
                raise HTTPException(status_code=404, detail=f"post with id:{id} not found")
            return deleted_post

@app.put("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_post(id: int, updated_post: Post):

    with psycopg2.connect(host="localhost", database="social", user="leo", 
    password="psw", cursor_factory=RealDictCursor) as postgres_connection:

        with postgres_connection.cursor() as cursor:

            cursor.execute("""UPDATE posts
                SET title = %s, content = %s, published = %s
                WHERE id = %s RETURNING *""", 
                (updated_post.title, updated_post.content, updated_post.published, str(id)))

            db_updated_post = cursor.fetchone()

            if not db_updated_post:
                raise HTTPException(status_code=404, detail=f"post with id:{id} not found")
            return db_updated_post
