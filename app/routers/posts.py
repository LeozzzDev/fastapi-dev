from fastapi import HTTPException, status, Depends, APIRouter
from ..database import get_db
from .. import models, schemas
from sqlalchemy.orm import Session
from typing import List

posts_router = APIRouter(prefix="/posts")

@posts_router.get("/", response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return posts

@posts_router.get("/{id}", response_model=schemas.Post)
async def get_post(id: int, db: Session = Depends(get_db)):
    found_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not found_post:
        raise HTTPException(status_code=404, detail=f"post with id:{id} not found")
    return found_post

@posts_router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.CreatePostRequest, db: Session = Depends(get_db)):
    created_post = models.Post(**post.dict())
    db.add(created_post)
    db.commit()
    db.refresh(created_post)
    return created_post

@posts_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    found_post = db.query(models.Post).filter(models.Post.id == id)
    
    if not found_post.first():
        raise HTTPException(status_code=404, detail=f"post with id:{id} not found")
    
    found_post.delete(synchronize_session=False)
    db.commit()

@posts_router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_post(id: int, updated_post: schemas.UpdatePostRequest, db: Session = Depends(get_db)):

    found_post = db.query(models.Post).filter(models.Post.id == id)

    if not found_post.first():
        raise HTTPException(status_code=404, detail=f"post with id:{id} not found")

    found_post.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return found_post.first()
