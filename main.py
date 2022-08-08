from random import randrange
from typing import Optional
from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

posts = []

app = FastAPI()

def get_post_by_id(id):
    for post in posts:
        if post['id'] == id:
            return post

def get_index_by_post_id(id):
    for i, post in enumerate(posts):
        if post['id'] == id:
            return i

@app.get("/")
async def get():
    return "try /posts"

@app.get("/posts")
async def get_posts():
    return {"data": posts}

@app.get("/posts/{id}")
async def get_post(id: int):
    post = get_post_by_id(id)
    if not post:
        raise HTTPException(status_code=404, detail=f"post with id:{id} not found")
    return post


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10)
    posts.append(post_dict)
    return post_dict

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    index = get_index_by_post_id(id)

    if index == None:
        raise HTTPException(status_code=404, 
            detail=f"post with id:{id} not found")

    posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_post(id: int, updated_post: Post):
    found_post_index = get_index_by_post_id(id)

    if found_post_index == None:
        raise HTTPException(status_code=404, 
            detail=f"post with id:{id} not found")

    updated_post_dict = updated_post.dict()
    updated_post_dict['id'] = id
    posts[found_post_index] = updated_post_dict
    return Response(status_code=status.HTTP_204_NO_CONTENT)