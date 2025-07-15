from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, DateTime, Boolean
from datetime import datetime, timezone
from typing import List

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)


class User(Base):
  __tablename__ = "users"
  
  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(String(150), nullable=False)
  username: Mapped[str] = mapped_column(String(150), nullable=False)
  email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
  password: Mapped[str] = mapped_column(String(150), nullable=False)
  created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=lambda: datetime.now(timezone.utc)
  )
  
  blogs: Mapped[List["Blog"]] = relationship(back_populates="author", cascade="all, delete-orphan")
  comments: Mapped[List["Comment"]] = relationship(back_populates="user", cascade="all, delete-orphan")
  likes: Mapped[List["Like"]] = relationship(back_populates="user", cascade="all, delete-orphan")



class Blog(Base):
  __tablename__ = "blogs"
  
  id: Mapped[int] = mapped_column(primary_key=True)
  title: Mapped[str] = mapped_column(String(100), nullable=False)
  body: Mapped[str] = mapped_column(String(5000), nullable=False)
  created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=lambda: datetime.now(timezone.utc)
  )
  updated_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=lambda: datetime.now(timezone.utc),
    onupdate=lambda: datetime.now(timezone.utc)
  )
  is_archived: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
  author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
  
  author: Mapped["User"] = relationship(back_populates="blogs")
  comments: Mapped[List["Comment"]] = relationship(back_populates="post", cascade="all, delete-orphan")
  likes: Mapped[List["Like"]] = relationship(back_populates="post", cascade="all, delete-orphan")



class Comment(Base):
  __tablename__ = "comments"
  
  id: Mapped[int] = mapped_column(primary_key=True)
  content: Mapped[str] = mapped_column(String(250), nullable=False)
  is_updated: Mapped[bool] = mapped_column(Boolean, default=False)
  created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=lambda: datetime.now(timezone.utc)
  )
  updated_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=lambda: datetime.now(timezone.utc),
    onupdate=lambda: datetime.now(timezone.utc)
  )
  is_archived: Mapped[bool] = mapped_column(Boolean, default=False)
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
  post_id: Mapped[int] = mapped_column(ForeignKey("blogs.id"))
  
  user: Mapped["User"] = relationship(back_populates="comments")
  post: Mapped["Blog"] = relationship(back_populates="comments")



class Like(Base):
  __tablename__ = "likes"
  __table_args__ = (
    db.UniqueConstraint("user_id", "post_id", name="unique_user_post_like"),
  )
  
  id: Mapped[int] = mapped_column(primary_key=True)
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
  post_id: Mapped[int] = mapped_column(ForeignKey("blogs.id"))
  created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=lambda: datetime.now(timezone.utc)
  )
  
  user: Mapped["User"] = relationship(back_populates="likes")
  post: Mapped["Blog"] = relationship(back_populates="likes")