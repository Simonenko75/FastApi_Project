import uuid
from datetime import datetime
from fastapi import APIRouter, Body, Depends, HTTPException
from starlette import status

from sqlalchemy import update, delete

from fastapi_app.forms import UserLoginForm, UserCreateForm, PostCreateForm
from fastapi_app.models import connect_db, User, AuthToken, Posts
from fastapi_app.utils import get_password_hash
from fastapi_app.auth import check_auth_token


router = APIRouter()


@router.get("/")
def read_root():
    return {"Hello": "World!!!"}


@router.get("/get/user/by/token")
def get_user(token: AuthToken = Depends(check_auth_token), database=Depends(connect_db)):
    user = database.query(User).filter(User.id == token.user_id).one_or_none()
    return {"id": user.id, "email": user.email, "nickname": user.nickname}


@router.post("/login")
def login(user_form: UserLoginForm = Body(..., embed=True), database=Depends(connect_db)):
    user = database.query(User).filter(User.email == user_form.email).one_or_none()
    if not user or get_password_hash(user_form.password) != user.password:
        return {"error": "Email/password invalid"}

    auth_token = AuthToken(token=str(uuid.uuid4()), user_id=user.id)
    database.add(auth_token)
    database.commit()
    return {"auth_token": auth_token.token}


@router.post("/create/user")
def create_user(user: UserCreateForm = Body(..., ember=True), database=Depends(connect_db)):
    exists_user = database.query(User.id).filter(User.email == user.email).one_or_none()
    if exists_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    new_user = User(
        email=user.email,
        password=get_password_hash(user.password),
        first_name=user.first_name,
        last_name=user.last_name,
        nickname=user.nickname
    )
    database.add(new_user)
    database.commit()

    return {"user_id": new_user.id}


@router.post("/create/post")
def create_post(post: PostCreateForm = Body(..., ember=True), database=Depends(connect_db)):

    new_post = Posts(
        title=post.title,
        subtitle=post.subtitle,
        author=post.author,
        content=post.content,
        completed=post.completed
    )
    database.add(new_post)
    database.commit()

    return {"post_title": new_post.title}


@router.put("/update/user/{user_id}")
def update_user(user_id: int, user: UserCreateForm = Body(..., ember=True), database=Depends(connect_db)):
    stmt = (
        update(User)
        .where(User.id == user_id)
        .values(email=user.email)
        .values(password=get_password_hash(user.password))
        .values(first_name=user.first_name)
        .values(last_name=user.last_name)
        .values(nickname=user.nickname)
        .values(created_at=datetime.now())
        .execution_options(synchronize_session="fetch")
    )

    database.execute(stmt)
    database.commit()

    return {
        "user_email": user.email,
        "user_password": user.password,
        "user_created": user.nickname,
    }


@router.put("/update/post/{post_id}")
def update_post(post_id: int, post: PostCreateForm = Body(..., ember=True), database=Depends(connect_db)):
    stmt = (
        update(Posts)
        .where(Posts.id == post_id)
        .values(title=post.title)
        .values(subtitle=post.subtitle)
        .values(author=post.author)
        .values(content=post.content,)
        .values(completed=post.completed)
        .values(created_at=datetime.now())
        .execution_options(synchronize_session="fetch")
    )

    database.execute(stmt)
    database.commit()

    return {
        "post_title": post.title,
        "post_author": post.author,
        "post_content": post.content,
    }


@router.delete("/delete/user/{user_id}")
def delete_user(user_id: int, database=Depends(connect_db)):
    stmt = (
        delete(User)
        .where(User.id == user_id)
        .execution_options(synchronize_session="fetch")
    )

    database.execute(stmt)
    database.commit()

    return {"Result": f"Successful delete user with id: {user_id}"}


@router.delete("/delete/post/{post_id}")
def delete_post(post_id: int, database=Depends(connect_db)):
    stmt = (
        delete(Posts)
        .where(Posts.id == post_id)
        .execution_options(synchronize_session="fetch")
    )

    database.execute(stmt)
    database.commit()

    return {"Result": f"Successful delete post with id: {post_id}"}
