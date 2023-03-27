from pydantic import BaseModel, Field
from typing import List, Union


class SignUpSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
    full_name: str = Field(...)
    email: str = Field(...)


class PostSchema(BaseModel):
    title: str = Field(...)
    content: str = Field(...)


class PostInDBSchema(PostSchema):
    author_id: int = Field(...)


class PostToUser(PostSchema):
    likes: int = Field(...)
    post_id: int = Field(...)
    comment: List[Union[str, None]] = Field(...)


class PostsSchema(BaseModel):
    posts: List[PostToUser]
