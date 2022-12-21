import hashlib

from fastapi_app.config import SECRET_KEY


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


def result_post(post_id, post):
    return {
        "Post": {
            "post_id": post_id,
            "post_title": post.title,
            "post_subtitle": post.subtitle,
            "post_author": post.author,
            "post_content": post.content,
            "post_completed": post.completed
        }
    }