from fastapi import FastAPI, HTTPException, status, Depends
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session
from typing import List

models.Base.metadata.create_all(bind=engine)

# postgres docker container
# docker run --name postgres-container -e POSTGRES_USER=leo -e POSTGRES_PASSWORD=psw -p 5432:5432 -v /data:/var/lib/postgresql/data -d postgres

app = FastAPI()

@app.get("/posts", response_model=List[schemas.PostResponse])
async def get_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return posts

@app.get("/posts/{id}", response_model=schemas.PostResponse)
async def get_post(id: int, db: Session = Depends(get_db)):
    found_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not found_post:
        raise HTTPException(status_code=404, detail=f"post with id:{id} not found")
    return found_post

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_post(post: schemas.CreatePostRequest, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    found_post = db.query(models.Post).filter(models.Post.id == id)
    
    if not found_post.first():
        raise HTTPException(status_code=404, detail=f"post with id:{id} not found")
    
    found_post.delete(synchronize_session=False)
    db.commit()

@app.put("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_post(id: int, updated_post: schemas.UpdatePostRequest, db: Session = Depends(get_db)):

    found_post = db.query(models.Post).filter(models.Post.id == id)

    if not found_post.first():
        raise HTTPException(status_code=404, detail=f"post with id:{id} not found")

    found_post.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return found_post.first()