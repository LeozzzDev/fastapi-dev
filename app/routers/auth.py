from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils, oauth2

auth_router = APIRouter(prefix="/auth")

@auth_router.post("/login")
async def login(user_login_request: schemas.UserLoginRequest, db: Session = Depends(get_db)):
    found_user = db.query(models.User).filter(models.User.email == user_login_request.email).first()

    if not found_user:
        raise HTTPException(status_code=403, detail=f"invalid credentials")
        
    if not utils.verify_password(user_login_request.password, found_user.password):
        raise HTTPException(status_code=403, detail=f"invalid credentials")
    
    data = { "user_id": found_user.id }

    jwt = oauth2.get_jwt(data)
    return {"token": jwt, "token_type": "bearer" }
