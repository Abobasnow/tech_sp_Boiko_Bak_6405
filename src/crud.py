from datetime import datetime, timedelta
from typing import Sequence

from sqlalchemy import select, func, delete
from sqlalchemy.orm import Session

from src import models


def create_account(db: Session, email: str, username: str, password: str) -> models.Account:
    account = models.Account(email=email, username=username, password=password)
    db.add(account)
    db.flush()
    return account


def get_account(db: Session, account_id: int) -> models.Account | None:
    return db.get(models.Account, account_id)


def get_account_by_email(db: Session, email: str) -> models.Account | None:
    return db.scalar(select(models.Account).where(models.Account.email == email))


def update_account(db: Session, account_id: int, **fields) -> models.Account | None:
    account = db.get(models.Account, account_id)
    if account is None:
        return None
    for key, value in fields.items():
        setattr(account, key, value)
    db.flush()
    return account


def delete_account(db: Session, account_id: int) -> bool:
    account = db.get(models.Account, account_id)
    if account is None:
        return False
    db.delete(account)
    db.flush()
    return True


def create_user(db: Session, account_id: int, nickname: str, **fields) -> models.User:
    user = models.User(account_id=account_id, nickname=nickname, **fields)
    db.add(user)
    db.flush()
    return user


def get_user(db: Session, user_id: int) -> models.User | None:
    return db.get(models.User, user_id)


def list_users(db: Session) -> Sequence[models.User]:
    return db.scalars(select(models.User)).all()


def update_user(db: Session, user_id: int, **fields) -> models.User | None:
    user = db.get(models.User, user_id)
    if user is None:
        return None
    for key, value in fields.items():
        setattr(user, key, value)
    db.flush()
    return user


def delete_user(db: Session, user_id: int) -> bool:
    user = db.get(models.User, user_id)
    if user is None:
        return False
    db.delete(user)
    db.flush()
    return True


def create_admin(db: Session, account_id: int, name: str, can_create_admins: bool = False, **fields) -> models.Admin:
    admin = models.Admin(
        account_id=account_id, name=name,
        can_create_admins=can_create_admins, **fields,
    )
    db.add(admin)
    db.flush()
    return admin


def get_admin(db: Session, admin_id: int) -> models.Admin | None:
    return db.get(models.Admin, admin_id)


def create_tag(db: Session, name: str, description: str | None = None) -> models.Tag:
    tag = models.Tag(name=name, description=description)
    db.add(tag)
    db.flush()
    return tag


def get_tag(db: Session, tag_id: int) -> models.Tag | None:
    return db.get(models.Tag, tag_id)


def get_tag_by_name(db: Session, name: str) -> models.Tag | None:
    return db.scalar(select(models.Tag).where(models.Tag.name == name))


def list_tags(db: Session) -> Sequence[models.Tag]:
    return db.scalars(select(models.Tag)).all()


def update_tag(db: Session, tag_id: int, **fields) -> models.Tag | None:
    tag = db.get(models.Tag, tag_id)
    if tag is None:
        return None
    for key, value in fields.items():
        setattr(tag, key, value)
    db.flush()
    return tag

def create_post(
    db: Session,
    title: str,
    body: str,
    tag_id: int | None = None,
    author_id: int | None = None,
    admin_id: int | None = None,
    **fields,
) -> models.Post:
    post = models.Post(
        title=title, body=body, tag_id=tag_id,
        author_id=author_id, admin_id=admin_id, **fields,
    )
    db.add(post)
    db.flush()
    return post


def get_post(db: Session, post_id: int) -> models.Post | None:
    return db.get(models.Post, post_id)


def list_published_posts(db: Session) -> Sequence[models.Post]:
    return db.scalars(
        select(models.Post)
        .where(models.Post.is_published.is_(True))
        .order_by(models.Post.published_at.desc())
    ).all()


def ts_by_tag(db: Session, tag_id: int) -> Sequence[models.Post]:
    return db.scalars(
        select(models.Post)
        .where(models.Post.tag_id == tag_id, models.Post.is_published.is_(True))
        .order_by(models.Post.published_at.desc())
    ).all()


def search_posts(db: Session, query: str) -> Sequence[models.Post]:
    pattern = f"%{query}%"
    return db.scalars(
        select(models.Post)
        .where(
            models.Post.is_published.is_(True),
            (models.Post.title.ilike(pattern) | models.Post.body.ilike(pattern)),
        )
    ).all()


def update_post(db: Session, post_id: int, **fields) -> models.Post | None:
    post = db.get(models.Post, post_id)
    if post is None:
        return None
    for key, value in fields.items():
        setattr(post, key, value)
    db.flush()
    return post


def publish_post(db: Session, post_id: int) -> models.Post | None:
    post = db.get(models.Post, post_id)
    if post is None:
        return None
    post.is_published = True
    post.status = "PUBLISHED"
    post.published_at = datetime.utcnow()
    db.flush()
    return post


def unpublish_post(db: Session, post_id: int) -> models.Post | None:
    post = db.get(models.Post, post_id)
    if post is None:
        return None
    post.is_published = False
    post.status = "ARCHIVED"
    db.flush()
    return post



def subscribe(db: Session, user_id: int, tag_id: int) -> models.Subscription:
    sub = models.Subscription(user_id=user_id, tag_id=tag_id)
    db.add(sub)
    db.flush()
    return sub


def unsubscribe(db: Session, user_id: int, tag_id: int) -> bool:
    sub = db.get(models.Subscription, (user_id, tag_id))
    if sub is None:
        return False
    db.delete(sub)
    db.flush()
    return True


def list_user_subscriptions(db: Session, user_id: int) -> Sequence[models.Subscription]:
    return db.scalars(
        select(models.Subscription).where(models.Subscription.user_id == user_id)
    ).all()


def list_tag_subscribers(db: Session, tag_id: int) -> Sequence[models.User]:
    return db.scalars(
        select(models.User)
        .join(models.Subscription, models.Subscription.user_id == models.User.id)
        .where(models.Subscription.tag_id == tag_id)
    ).all()



def record_view(db: Session, post_id: int, user_id: int | None, read_seconds: int = 0) -> models.ViewHistory:
    view = models.ViewHistory(user_id=user_id, post_id=post_id, read_seconds=read_seconds)
    db.add(view)
    db.flush()
    return view


def count_views(db: Session, post_id: int) -> int:
    return db.scalar(
        select(func.count(models.ViewHistory.id)).where(models.ViewHistory.post_id == post_id)
    ) or 0


def user_recent_views(db: Session, user_id: int, limit: int = 20) -> Sequence[models.ViewHistory]:
    return db.scalars(
        select(models.ViewHistory)
        .where(models.ViewHistory.user_id == user_id)
        .order_by(models.ViewHistory.viewed_at.desc())
        .limit(limit)
    ).all()


def add_to_library(db: Session, user_id: int, post_id: int) -> models.UserPostLibrary:
    entry = models.UserPostLibrary(user_id=user_id, post_id=post_id)
    db.add(entry)
    db.flush()
    return entry


def remove_from_library(db: Session, user_id: int, post_id: int) -> bool:
    entry = db.get(models.UserPostLibrary, (user_id, post_id))
    if entry is None:
        return False
    db.delete(entry)
    db.flush()
    return True


def list_user_library(db: Session, user_id: int) -> Sequence[models.Post]:
    return db.scalars(
        select(models.Post)
        .join(models.UserPostLibrary, models.UserPostLibrary.post_id == models.Post.id)
        .where(models.UserPostLibrary.user_id == user_id)
        .order_by(models.UserPostLibrary.added_at.desc())
    ).all()