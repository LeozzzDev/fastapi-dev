from fastapi import HTTPException, status, Depends, APIRouter
from ..database import get_db
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

@router.get("/users", response_model=List[schemas.User])
async def get_users(db: Session = Depends(get_db)):
    posts = db.query(models.User).all()
    return posts
    
@router.get("/users/{id}", response_model=schemas.User)
async def get_user(id: int, db: Session = Depends(get_db)):
    found_user = db.query(models.User).filter(models.User.id == id).first()
    if not found_user:
        raise HTTPException(status_code=404, detail=f"user with id:{id} not found")
    return found_user

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
async def create_user(user: schemas.CreateUserRequest, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    created_user = models.User(**user.dict())
    db.add(created_user)
    db.commit()
    db.refresh(created_user)
    return created_user

@router.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, db: Session = Depends(get_db)):
    found_user = db.query(models.User).filter(models.User.id == id)

    if not found_user.first():
        raise HTTPException(status_code=404, detail=f"user with id:{id} not found")

    found_user.delete(synchronize_session=False)
    db.commit()

@router.put("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(id: int, updated_user: schemas.UpdateUSerRequest, db: Session = Depends(get_db)):

    found_user = db.query(models.User).filter(models.User.id == id)

    if not found_user.first():
        raise HTTPException(status_code=404, detail=f"user with id:{id} not found")

    found_user.update(updated_user.dict(), synchronize_session=False)
    db.commit()
    return found_user.first()