from fastapi import Depends
from fastapi import APIRouter
from fastapi import HTTPException

from sqlalchemy.orm import Session

from ..database import get_db
from ..services import post_crud
from ..services import user_crud

from ..jwt_encrypt import get_current_user

from ..schemas.user_schema import UserInfo
from ..schemas.post_schema import PostInfo
from ..schemas.post_schema import PostCreate
from ..schemas.post_schema import PostIdItem

post_router = APIRouter()


@post_router.post("/post", response_model=PostInfo, status_code=201)
def create_post(post: PostCreate, current_user: UserInfo = Depends(get_current_user), db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_id(current_user.id, db=db)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User with this id does not exist")
    return post_crud.create_post(post=post, user_id=current_user.id, db=db)


@post_router.post('/post/like')
def like_post(post: PostIdItem, current_user: UserInfo = Depends(get_current_user), db: Session = Depends(get_db)):
    db_post = post_crud.get_post_by_id(post_id=post.post_id, db=db)
    if db_post is None:
        raise HTTPException(status_code=400, detail="Post with this id does not exist")
    return post_crud.like_post(post_id=post.post_id, user_id=current_user.id, db=db)


@post_router.post('/post/dislike')
def dislike_post(post: PostIdItem, current_user: UserInfo = Depends(get_current_user), db: Session = Depends(get_db)):
    db_post = post_crud.get_post_by_id(post_id=post.post_id, db=db)
    if db_post is None:
        raise HTTPException(status_code=400, detail="Post with this id does not exist")
    return post_crud.dislike_post(post_id=post.post_id, user_id=current_user.id, db=db)


@post_router.get('/post/analytics/{date_from}/{date_to}')
def analyze_total_likes(date_from: int, date_to: int, current_user: UserInfo = Depends(get_current_user), db: Session = Depends(get_db)):
    return post_crud.analyze_total_likes(
        date_from=date_from,
        date_to=date_to,
        user_id=current_user.id,
        db=db
    )
