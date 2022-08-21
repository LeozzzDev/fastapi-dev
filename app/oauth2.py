from datetime import datetime
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_jwt(data: dict):
    to_encode = data.copy()
    expiration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expiration})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_jwt(token: str, jwt_exception):
    try:
        decoded_jwt_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = decoded_jwt_data.get("user_id")

        if user_id is None:
            raise jwt_exception

        token_data = schemas.TokenData(id=user_id)
    
    except JWTError:
        raise jwt_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    jwt_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Unauthorized!",
        headers={"WWW-Authenticate": "Bearer"})
    
    return verify_jwt(token, jwt_exception)




