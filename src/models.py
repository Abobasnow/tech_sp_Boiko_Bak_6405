from datetime import datetime
from sqlalchemy import (
    BigInteger, Boolean, DateTime, ForeignKey, Integer,
    String, Text, UniqueConstraint, func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base


class Account(Base):
    __tablename__ = "account"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="account", uselist=False)
    admin: Mapped["Admin"] = relationship(back_populates="account", uselist=False)

    def __repr__(self) -> str:
        return f"<Account id={self.id} email={self.email}>"


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    nickname: Mapped[str] = mapped_column(String(150), nullable=False)
    avatar_url: Mapped[str | None] = mapped_column(String(500))
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
    account_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("account.id"), unique=True, nullable=False
    )

    account: Mapped[Account] = relationship(back_populates="user")
    posts: Mapped[list["Post"]] = relationship(
        back_populates="author", foreign_keys="Post.author_id"
    )
    subscriptions: Mapped[list["Subscription"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    views: Mapped[list["ViewHistory"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    library: Mapped[list["UserPostLibrary"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} nickname={self.nickname}>"


class Admin(Base):
    __tablename__ = "admin"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    can_create_admins: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    avatar_url: Mapped[str | None] = mapped_column(String(500))
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
    account_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("account.id"), unique=True, nullable=False
    )

    account: Mapped[Account] = relationship(back_populates="admin")
    posts: Mapped[list["Post"]] = relationship(
        back_populates="admin", foreign_keys="Post.admin_id"
    )

    def __repr__(self) -> str:
        return f"<Admin id={self.id} name={self.name}>"


class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)

    posts: Mapped[list["Post"]] = relationship(back_populates="tag")
    subscriptions: Mapped[list["Subscription"]] = relationship(
        back_populates="tag", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Tag id={self.id} name={self.name}>"


class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    author_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("user.id"))
    admin_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("admin.id"))
    tag_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("tag.id"))
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    summary: Mapped[str | None] = mapped_column(Text)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    cover_url: Mapped[str | None] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="DRAFT")
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    published_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    author: Mapped[User | None] = relationship(back_populates="posts", foreign_keys=[author_id])
    admin: Mapped[Admin | None] = relationship(back_populates="posts", foreign_keys=[admin_id])
    tag: Mapped[Tag | None] = relationship(back_populates="posts")
    views: Mapped[list["ViewHistory"]] = relationship(
        back_populates="post", cascade="all, delete-orphan"
    )
    in_libraries: Mapped[list["UserPostLibrary"]] = relationship(
        back_populates="post", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Post id={self.id} title={self.title!r}>"


class Subscription(Base):
    __tablename__ = "subscription"

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id"), primary_key=True
    )
    tag_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("tag.id"), primary_key=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    user: Mapped[User] = relationship(back_populates="subscriptions")
    tag: Mapped[Tag] = relationship(back_populates="subscriptions")


class ViewHistory(Base):
    __tablename__ = "view_history"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("post.id"), nullable=False)
    viewed_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    read_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    user: Mapped[User | None] = relationship(back_populates="views")
    post: Mapped[Post] = relationship(back_populates="views")


class UserPostLibrary(Base):
    __tablename__ = "user_post_library"

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id"), primary_key=True
    )
    post_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("post.id"), primary_key=True
    )
    added_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    user: Mapped[User] = relationship(back_populates="library")
    post: Mapped[Post] = relationship(back_populates="in_libraries")