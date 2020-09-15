from datetime import datetime
from pydantic import Field
from pydantic import BaseModel


class PostBase(BaseModel):
    title: str = Field(min_length=4)
    text: str = None


class PostCreate(PostBase):
    pass


class PostInfo(PostBase):
    id: int
    user_id: int
    timestamp: datetime

    class Config:
        orm_mode = True


class PostIdItem(BaseModel):
    post_id: int
