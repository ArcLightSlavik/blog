from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    last_login_time = Column(DateTime, nullable=True)
    last_request_time = Column(DateTime, nullable=True)

    posts = relationship('Post')
    likes = relationship('Like')
