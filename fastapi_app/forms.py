from pydantic import BaseModel
from typing import Optional


class UserLoginForm(BaseModel):
    email: str
    password: str


class UserCreateForm(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: Optional[str] = None
    nickname: Optional[str] = None


class PostCreateForm(BaseModel):
    title: str
    subtitle: Optional[str] = None
    author_email: str
    content: str
    completed: bool


class CommentCreateForm(BaseModel):
    author_email: str
    comment_text: str
