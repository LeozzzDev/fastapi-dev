from datetime import datetime
from jose import JWTError, jwt
from datetime import datetime, timedelta
from config import settings
from . import models
from . import schemas, database
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_jwt(data: dict):
    to_encode = data.copy()
    expiration = datetime.utcnow() + timedelta(minutes=settings.jwt_access_token_expire_minutes)
    to_encode.update({"exp": expiration})
    
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt

def verify_jwt(token: str, jwt_exception):
    try:
        decoded_jwt_data = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        user_id = decoded_jwt_data.get("user_id")

        if user_id is None:
            raise jwt_exception

        token_data = schemas.TokenData(id=user_id)
    
    except JWTError:
        raise jwt_exception

    return token_data

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(database.get_db)
):
    jwt_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Unauthorized!",
        headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_jwt(token, jwt_exception)
    
    current_user = db.query(models.User).filter(models.User.id == token.id).first()
    return current_user




