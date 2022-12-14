import hashlib
import uuid

from fastapi_app.config import SECRET_KEY
from fastapi_app.models import User, AuthToken


def get_password_hash(password: str) -> str:
    return hashlib.sha256(f"{SECRET_KEY}{password}".encode("utf-8")).hexdigest()


def result_user(user_id, user):
    return {
        "User": {
            "user_id": user_id,
            "user_email": user.email,
            "user_password": user.password,
            "user_first_name": user.first_name,
            "user_last_name": user.last_name,
            "user_nickname": user.nickname
        }
    }


def result_post(post_id, post, user_name):
    return {
        "Post": {
            "post_id": post_id,
            "post_title": post.title,
            "post_subtitle": post.subtitle,
            "post_author": user_name,
            "post_author_email": post.author_email,
            "post_content": post.content,
            "post_completed": post.completed
        }
    }


def result_comment(comment_id, comment, user_name):
    return {
        "Comment": {
            "comment_id": comment_id,
            "comment_author": user_name,
            "author_email": comment.author_email,
            "comment_text": comment.comment_text
        }
    }


def login_auto(login_form, database):
    user = database.query(User).filter(User.email == login_form.email).one_or_none()
    if not user or get_password_hash(login_form.password) != user.password:
        return {"error": "Email/password invalid"}

    auth_token = AuthToken(token=str(uuid.uuid4()), user_id=user.id)
    database.add(auth_token)
    database.commit()
    return {"auth_token": auth_token.token}


def return_token(user_id, user, database):
    auth_token = database.query(AuthToken).filter(AuthToken.user_id == user_id).one_or_none()

    if not auth_token:
        user_login = User(
            email=user.email,
            password=user.password
        )

        token = login_auto(user_login, database)
        return token
    return auth_token.token
