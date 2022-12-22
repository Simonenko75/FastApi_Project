from datetime import datetime
from enum import Enum

from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

from fastapi_app.config import DATABASE_URL


Base = declarative_base()


class StreamStatus(Enum):
    PLANED = "planed"
    ACTIVE = "active"
    CLOSED = "closed"


def connect_db():
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    session = Session(bind=engine.connect())
    return session


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    nickname = Column(String)
    created_at = Column(String, default=datetime.utcnow())


class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    subtitle = Column(String)
    author = Column(String, ForeignKey("users.first_name"))
    author_email = Column(String, ForeignKey("users.email"))
    content = Column(String)
    completed = Column(Boolean)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(String, default=datetime.utcnow())


class AuthToken(Base):
    __tablename__ = "auth_token"

    id = Column(Integer, primary_key=True)
    token = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(String, default=datetime.utcnow())


class Comments(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    subtitle = Column(String)
    author_comment = Column(String, ForeignKey("users.first_name"))
    author_email = Column(String, ForeignKey("users.email"))
    comment_text = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("post.id"))
    created_at = Column(String, default=datetime.utcnow())
