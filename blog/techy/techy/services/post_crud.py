from typing import Dict
from datetime import datetime

from sqlalchemy.orm import Session

from .user_crud import update_user_last_action

from ..models import post_model, like_model
from ..schemas import post_schema
from ..exceptions import LikeException


def get_post_by_id(post_id: int, db: Session) -> post_model.Post:
    return db.query(post_model.Post).filter(post_model.Post.id == post_id).first()


def create_post(post: post_schema.PostCreate, user_id: int, db: Session) -> post_model.Post:
    db_post = post_model.Post(
        title=post.title,
        text=post.text,
        timestamp=datetime.now(),
        user_id=user_id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    update_user_last_action(user_id=user_id, db=db)
    return db_post


def like_post(post_id: int, user_id: int, db: Session) -> like_model.Like:
    prevent_double_action(action_type=1, post_id=post_id, user_id=user_id, db=db)
    db_like = like_model.Like(
        user_id=user_id,
        post_id=post_id,
        timestamp=datetime.now(),
        type=True
    )
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    update_user_last_action(user_id=user_id, db=db)
    return db_like


def dislike_post(post_id: int, user_id: int, db: Session) -> like_model.Like:
    prevent_double_action(action_type=0, post_id=post_id, user_id=user_id, db=db)
    db_dislike = like_model.Like(
        user_id=user_id,
        post_id=post_id,
        timestamp=datetime.now(),
        type=False
    )
    db.add(db_dislike)
    db.commit()
    db.refresh(db_dislike)
    update_user_last_action(user_id=user_id, db=db)
    return db_dislike


def analyze_total_likes(date_from: int, date_to: int, user_id: int, db: Session) -> Dict[str, int]:
    datetime_from = datetime.fromtimestamp(date_from)
    datetime_to = datetime.fromtimestamp(date_to)
    likes = db.query(like_model.Like) \
        .filter(like_model.Like.timestamp > datetime_from) \
        .filter(like_model.Like.timestamp < datetime_to) \
        .filter(like_model.Like.type == 1) \
        .all()
    dislikes = db.query(like_model.Like) \
        .filter(like_model.Like.timestamp > datetime_from) \
        .filter(like_model.Like.timestamp < datetime_to) \
        .filter(like_model.Like.type == 0) \
        .all()
    update_user_last_action(user_id=user_id, db=db)
    # can return a detail of each like/dislike or just the number of them
    return dict(likes=len(likes), dislikes=len(dislikes))


def prevent_double_action(action_type: int, post_id: int, user_id: int, db: Session):
    # Prevent person from mass disliking post
    previous_actions = db.query(like_model.Like) \
        .filter(like_model.Like.post_id == post_id) \
        .filter(like_model.Like.user_id == user_id) \
        .all()
    if previous_actions:
        if previous_actions[-1].type == action_type:
            raise LikeException
