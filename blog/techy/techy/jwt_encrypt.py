import jwt

from datetime import timedelta, datetime

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from .database import get_db
from .exceptions import CredentialsException

from .schemas.user_schema import TokenData
from .services.user_crud import get_user_by_username

secret_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9"
algorithm = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authenticate")


def create_access_token(data: dict, expires_delta: timedelta = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    data.update(dict(exp=expire))
    encoded_jwt = jwt.encode(data, secret_key, algorithm=algorithm)
    return encoded_jwt


def decode_access_token(data: str):
    return jwt.decode(data, secret_key, algorithm=algorithm)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_access_token(data=token)
        username: str = payload.get("sub")
        if username is None:
            raise CredentialsException
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise CredentialsException
    user = get_user_by_username(username=token_data.username, db=db)
    if user is None:
        raise CredentialsException
    return user
