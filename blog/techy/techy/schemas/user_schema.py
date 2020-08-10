from typing import List

from datetime import datetime
from pydantic import BaseModel, Field
from .post_schema import PostInfo


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserAuthenticate(UserBase):
    password: str = Field(min_length=8)


class UserInfo(UserBase):
    id: int
    posts: List[PostInfo] = None

    class Config:
        orm_mode = True


class UserAnalytics(UserInfo):
    last_login_time: datetime = None
    last_request_time: datetime = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None
