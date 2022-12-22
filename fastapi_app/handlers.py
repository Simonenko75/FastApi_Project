from datetime import datetime
from fastapi import APIRouter, Body, Depends, HTTPException
from starlette import status

from sqlalchemy import update, delete

from fastapi_app.forms import UserCreateForm, PostCreateForm, CommentCreateForm
from fastapi_app.models import connect_db, User, AuthToken, Posts, Comments
from fastapi_app.utils import get_password_hash, result_user, result_post, login_auto, return_token, result_comment
from fastapi_app.auth import check_auth_token


router = APIRouter()


@router.get("/")
def read_root():
    return {"Hello": "World!!!"}


@router.get("/get/user/by/token")
def get_user_by_token(token: AuthToken = Depends(check_auth_token), database=Depends(connect_db)):
    user = database.query(User).filter(User.id == token.user_id).one_or_none()
    return {"id": user.id, "email": user.email, "nickname": user.nickname}


@router.get("/get/user/by/id/{user_id}")
def get_user_by_id(user_id: int, database=Depends(connect_db)):
    user = database.query(User).filter(User.id == user_id).one_or_none()

    try:
        result = result_user(user_id, user)
    except:
        return "No user as this in DB!"

    return result


@router.get("/get/post/by/id/{post_id}")
def get_post_by_id(post_id: int, database=Depends(connect_db)):
    post = database.query(Posts).filter(Posts.id == post_id).one_or_none()

    try:
        result = result_post(post_id, post)
    except:
        return "No user as this in DB!"

    return result


@router.get("/get/comment/by/id/{comment_id}")
def get_post_by_id(comment_id: int, database=Depends(connect_db)):
    comment = database.query(Comments).filter(Comments.id == comment_id).one_or_none()

    try:
        result = result_post(comment_id, comment)
    except:
        return "No comment as this in DB!"

    return result


@router.post("/create/user")
def create_user(user: UserCreateForm = Body(..., ember=True), database=Depends(connect_db)):
    exists_user = database.query(User).filter(User.email == user.email).one_or_none()
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

    user_login = User(
        email=user.email,
        password=user.password
    )

    auth_token = login_auto(user_login, database)

    user1 = database.query(User).filter(User.email == user.email).one_or_none()
    try:
        result = result_user(user1.id, user)
    except:
        return "No post as this in DB!"

    return result, {"auth_token": auth_token}


@router.post("/create/post")
def create_post(post: PostCreateForm = Body(..., ember=True), database=Depends(connect_db)):
    user = database.query(User).filter(User.email == post.author_email).one_or_none()

    if user:
        new_post = Posts(
            title=post.title,
            subtitle=post.subtitle,
            author=user.first_name,
            author_email=post.author_email,
            content=post.content,
            completed=post.completed,
            user_id=user.id
        )

        database.add(new_post)
        database.commit()

        post1 = database.query(Posts).filter(Posts.content == post.content).one_or_none()
        try:
            result = result_post(post1.id, post, user.first_name)
        except:
            return "No post as this in DB!"

        return result
    else:
        return "User with this email not exists!" '\n'\
               "Before You must create user. '\n'" \
               "Probable You have some mistakes, check please."


@router.post("/create/comment")
def create_comment(comment: CommentCreateForm = Body(..., ember=True), database=Depends(connect_db)):
    user = database.query(User).filter(User.email == comment.author_email).one_or_none()

    if user:
        new_comment = Comments(
            author=user.first_name,
            author_email=comment.author_email,
            content=comment.comment_text,
            user_id=user.id
        )

        database.add(new_comment)
        database.commit()

        comment1 = database.query(Posts).filter(Comments.comment_text == comment.comment_text).one_or_none()
        try:
            result = result_comment(comment1.id, comment, user.first_name)
        except:
            return "No comment as this in DB!"

        return result
    else:
        return "Comment with this email not exists!" '\n'\
               "Probable You have some mistakes, check please."


@router.put("/update/user/{user_id}")
def update_user(user_id: int, user: UserCreateForm = Body(..., ember=True), database=Depends(connect_db)):
    user_correct = database.query(User).filter(User.id == user_id).one_or_none()
    if user_correct:
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

        token = return_token(user_id, user, database)

        try:
            result = result_user(user_id, user)
        except:
            return "No user as this in DB!"

        return result, {"auth_token": token}
    else:
        return "User with this email not correct!" '\n'\
               "Probable You have some mistakes, check email please."


@router.put("/update/post/{post_id}")
def update_post(post_id: int, post: PostCreateForm = Body(..., ember=True), database=Depends(connect_db)):
    user = database.query(User).filter(User.email == post.author_email).one_or_none()

    if user:
        stmt = (
            update(Posts)
            .where(Posts.id == post_id)
            .values(title=post.title)
            .values(subtitle=post.subtitle)
            .values(author=user.first_name)
            .values(author_email=post.author_email)
            .values(content=post.content)
            .values(completed=post.completed)
            .values(created_at=datetime.now())
            .execution_options(synchronize_session="fetch")
        )

        database.execute(stmt)
        database.commit()

        try:
            result = result_post(post_id, post, user.first_name)
        except:
            return "No post as this in DB!"

        return result
    else:
        return "Post with this email not exists!" '\n'\
               "Probable You have some mistakes, check please."


@router.put("/update/comment/{comment_id}")
def update_post(comment_id: int, comment: CommentCreateForm = Body(..., ember=True), database=Depends(connect_db)):
    user = database.query(User).filter(User.email == comment.author_email).one_or_none()

    if user:
        stmt = (
            update(Comments)
            .where(Comments.id == comment_id)
            .values(author=user.first_name)
            .values(author_email=comment.author_email)
            .values(content=comment.comment_text)
            .values(created_at=datetime.now())
            .execution_options(synchronize_session="fetch")
        )

        database.execute(stmt)
        database.commit()

        try:
            result = result_comment(comment_id, comment, user.first_name)
        except:
            return "No comment as this in DB!"

        return result
    else:
        return "Comment with this email not exists!" '\n'\
               "Probable You have some mistakes, check please."


@router.delete("/delete/user/{user_id}")
def delete_user(user_id: int, database=Depends(connect_db)):
    exists_user = database.query(User).filter(User.id == user_id).one_or_none()

    if exists_user:
        stmt = (
            delete(User)
            .where(User.id == user_id)
            .execution_options(synchronize_session="fetch")
        )

        database.execute(stmt)
        database.commit()

        return {"Result": f"Successful delete user with id: {user_id}"}
    else:
        return "Please try again, but with correct id. User with this id is not in DB!"


@router.delete("/delete/post/{post_id}")
def delete_post(post_id: int, database=Depends(connect_db)):
    exists_post = database.query(Posts).filter(Posts.id == post_id).one_or_none()

    if exists_post:
        stmt = (
            delete(Posts)
            .where(Posts.id == post_id)
            .execution_options(synchronize_session="fetch")
        )

        database.execute(stmt)
        database.commit()

        return {"Result": f"Successful delete post with id: {post_id}"}
    else:
        return "Please try again, but with correct id. Post with this id is not in DB!"


@router.delete("/delete/comment/{comment_id}")
def delete_post(comment_id: int, database=Depends(connect_db)):
    exists_comment = database.query(Posts).filter(Posts.id == comment_id).one_or_none()

    if exists_comment:
        stmt = (
            delete(Comments)
            .where(Comments.id == comment_id)
            .execution_options(synchronize_session="fetch")
        )

        database.execute(stmt)
        database.commit()

        return {"Result": f"Successful delete comment with id: {comment_id}"}
    else:
        return "Please try again, but with correct id. Comment with this id is not in DB!"
