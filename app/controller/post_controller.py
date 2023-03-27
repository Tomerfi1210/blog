from app.controller.blog_controller import BlogController
from app.tables import Post
from app.db import get_session
from app.schema.model import PostInDBSchema, PostToUser, PostSchema
from app.tables import Post, Comment
from fastapi import HTTPException, status
from sqlalchemy import select, insert, delete, update, func
from typing import List


class PostController(BlogController):
    def __init__(self) -> None:
        super().__init__()

    async def create_post(self, post_schema: PostInDBSchema) -> int:
        statement = insert(Post).values(
            title=post_schema.title,
            content=post_schema.content,
            author_id=post_schema.author_id,
        )

        async_session = await get_session()

        async with async_session() as session:
            async with session.begin():
                res = await session.execute(statement=statement)
                await session.commit()

        return res.inserted_primary_key[0]

    async def edit_post(self, post_id, user_id, post_schema: PostSchema) -> None:
        update_post = (
            update(Post)
            .values(
                title=post_schema.title,
                content=post_schema.content,
            )
            .where((Post.id == post_id) & (Post.author_id == user_id))
        )

        async_session = await get_session()

        async with async_session() as session:
            async with session.begin():
                res = await session.execute(statement=update_post)
                await session.commit()

        if res.rowcount == 0:  # no update
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect post_id or user not authorize to edit post",
                headers={"WWW-Authenticate": "Bearer"},
            )

    async def get_all_posts(self) -> List[PostToUser]:
        statement = (
            select(Post, func.array_agg(Comment.comment).label("comments"))
            .join(Comment, Post.id == Comment.post_id, isouter=True)
            .group_by(Post.id)
            .order_by(Post.id)
        )

        async_session = await get_session()

        async with async_session() as session:
            async with session.begin():
                posts = await session.execute(statement=statement)
                posts = posts.all()

                posts = [
                    PostToUser(
                        title=post.title,
                        content=post.content,
                        likes=post.likes,
                        post_id=post.id,
                        comment=comment,
                    )
                    for post, comment in posts
                ]
        return posts

    async def delete_post(self, post_id, possible_author_id) -> None:
        statement = delete(Post).where(
            (Post.id == post_id) & (Post.author_id == possible_author_id)
        )

        async_session = await get_session()

        async with async_session() as session:
            async with session.begin():
                res = await session.execute(statement)
                await session.commit()

        if res.rowcount == 0:  # no delete
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect post_id",
                headers={"WWW-Authenticate": "Bearer"},
            )

    async def get_post(self, post_id: int, user_id: int):
        async_session = await get_session()

        async with async_session() as session:
            async with session.begin():
                post = await session.get(Post, post_id)
                await session.commit()

        if not post:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Post not Exist",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return post
