from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    Boolean,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.sql import func
import os

load_dotenv()

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    password = Column(String)
    full_name = Column(String, default=None)
    email = Column(String, unique=True)
    date_registration = Column(Date, default=func.now())
    disabled = Column(Boolean, default=False)


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    content = Column(String)
    author_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"), nullable=False)
    user = relationship("User", backref="posts")

    creation_date = Column(Date, default=func.now())
    likes = Column(Integer, default=0)


class Like(Base):
    __tablename__ = "like"

    post_id = Column(Integer, ForeignKey(Post.id, ondelete="CASCADE"), nullable=False)
    user_id = Column(
        Integer, ForeignKey(User.id, ondelete="CASCADE"), nullable=False
    )  # who gave the like
    user = relationship("User", backref="like")
    post = relationship("Post", backref="like")

    __table_args__ = (
        PrimaryKeyConstraint("post_id", "user_id"),
        {},
    )


class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey(Post.id, ondelete="CASCADE"), nullable=False)
    user_id = Column(
        Integer, ForeignKey(User.id, ondelete="CASCADE"), nullable=False
    )  # who gave the comment
    comment = Column(String)
    user = relationship("User", backref="comment")
    post = relationship("Post", backref="comment")


path = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}:5432/{os.environ['POSTGRES_DB']}"
print(path)
engine = create_engine(path, echo=True)
Base.metadata.create_all(engine)
