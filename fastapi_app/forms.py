from pydantic import BaseModel
from typing import Optional


class UserLoginForm(BaseModel):
    email: str
    password: str


class UserCreateForm(BaseModel):
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    nickname: Optional[str] = None


class PostCreateForm(BaseModel):
    title: str
    subtitle: Optional[str] = None
    author: str
    content: str
    completed: bool
