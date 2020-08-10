from sqlalchemy import Column, Integer, Boolean, ForeignKey, DateTime

from .user_model import Base


class Like(Base):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    type = Column(Boolean, nullable=False)
    timestamp = Column(DateTime, nullable=False)
