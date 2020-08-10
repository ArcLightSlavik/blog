import bcrypt

from typing import Dict
from datetime import datetime
from sqlalchemy.orm import Session

from ..models import user_model, post_model
from ..schemas import user_schema


def get_user_by_username(username: str, db: Session) -> user_model.User:
    return db.query(user_model.User).filter(user_model.User.username == username).first()


def get_user_by_id(user_id: int, db: Session) -> user_model.User:
    return db.query(user_model.User).filter(user_model.User.id == user_id).first()


def get_user_analytics(user: user_schema.UserAnalytics, db: Session) -> Dict:
    update_user_last_action(user.id, db)
    return dict(last_login=user.last_login_time, last_request=user.last_request_time)


def get_all_user_posts(user_id: int, db: Session) -> post_model.Post:
    update_user_last_action(user_id=user_id, db=db)
    return db.query(post_model.Post).filter(post_model.Post.user_id == user_id).all()


def create_user(user: user_schema.UserCreate, db: Session) -> user_model.User:
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = user_model.User(
        username=user.username,
        password=hashed_password,
        last_login_time=datetime.now(),
        last_request_time=datetime.now()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def check_username_password(user: user_schema.UserAuthenticate, db: Session) -> bool:
    db_user_info = get_user_by_username(username=user.username, db=db)
    update_user_last_login(user_id=db_user_info.id, db=db)
    update_user_last_action(user_id=db_user_info.id, db=db)
    return bcrypt.checkpw(user.password.encode('utf-8'), db_user_info.password)


def update_user_last_login(user_id: int, db: Session) -> None:
    db_user = get_user_by_id(user_id=user_id, db=db)
    db_user.last_login_time = datetime.now()
    db.commit()


def update_user_last_action(user_id: int, db: Session) -> None:
    db_user = get_user_by_id(user_id=user_id, db=db)
    db_user.last_request_time = datetime.now()
    db.commit()
