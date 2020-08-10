from typing import List
from fastapi import Depends, HTTPException, APIRouter
from datetime import timedelta

from sqlalchemy.orm import Session

from ..database import get_db
from ..services import user_crud
from ..jwt_encrypt import create_access_token, get_current_user

from ..schemas.user_schema import UserInfo, UserCreate, UserAuthenticate
from ..schemas.post_schema import PostInfo

user_router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30


@user_router.post("/user", response_model=UserInfo, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_username(username=user.username, db=db)
    if db_user:
        raise HTTPException(status_code=400, detail="User with this username has already been registered")
    return user_crud.create_user(db=db, user=user)


@user_router.post("/authenticate")
def authenticate_user(user: UserAuthenticate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_username(username=user.username, db=db)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User with this username does not exist")

    correct_password = user_crud.check_username_password(user=user, db=db)
    if correct_password is False:
        raise HTTPException(status_code=400, detail="Password is not correct")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data=dict(sub=user.username), expires_delta=access_token_expires)
    return dict(access_token=access_token, token_type="Bearer")


@user_router.get("/user/info", response_model=UserInfo)
def get_user_by_id(current_user: UserInfo = Depends(get_current_user), db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_id(user_id=current_user.id, db=db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@user_router.get("/user/analytics")
def get_user_analytics(current_user: UserInfo = Depends(get_current_user), db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_id(user_id=current_user.id, db=db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_crud.get_user_analytics(user=db_user, db=db)


@user_router.get("/user/posts", response_model=List[PostInfo])
def get_all_user_posts(current_user: UserInfo = Depends(get_current_user), db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_id(user_id=current_user.id, db=db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_crud.get_all_user_posts(user_id=current_user.id, db=db)
