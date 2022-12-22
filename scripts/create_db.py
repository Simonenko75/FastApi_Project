from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fastapi_app.config import DATABASE_URL


def main():
    engine = create_engine(DATABASE_URL)
    session = Session(bind=engine.connect())

    session.execute("""create table users (
    id integer not null primary key,
    email varchar(256),
    password varchar(256),
    first_name varchar(256),
    last_name varchar(256),
    nickname varchar(256),
    created_at varchar(256)
    );""")

    session.execute("""create table posts (
        id integer not null primary key,
        title varchar(256),
        subtitle varchar(256),
        author varchar(256) references users,
        content varchar(256),
        completed varchar(256),
        user_id integer references users,
        created_at varchar(256)
        );""")

    session.execute("""create table auth_token (
    id integer not null primary key,
    token varchar(256),
    user_id integer references users,
    created_at varchar(256)
    );""")

    session.execute("""create table comments (
        id integer not null primary key,
        title varchar(256),
        subtitle varchar(256),
        author_comment varchar(256) references users,
        comment_text varchar(256),
        user_id integer references users,
        post_id integer references posts,
        created_at varchar(256)
        );""")

    session.close()


if __name__ == "__main__":
    main()