from datetime import datetime
from pydantic import BaseModel


class LikeBase(BaseModel):
    type: bool = False


class LikeCreate(LikeBase):
    pass


class LikeInfo(LikeBase):
    id: int
    user_id: int
    post_id: int
    timestamp: datetime

    class Config:
        orm_mode = True
