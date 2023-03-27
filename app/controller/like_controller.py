from app.controller.blog_controller import BlogController
from app.db import get_session
from app.tables import Post, Like
from fastapi import HTTPException, status
from sqlalchemy import select, insert, delete, update


class LikeController(BlogController):
    async def like_post(self, post_id, user_id):
        increment_like = (
            update(Post).values(likes=Post.likes + 1).where(Post.id == post_id)
        )
        add_to_like_table = insert(Like).values(post_id=post_id, user_id=user_id)

        async_session = await get_session()

        async with async_session() as session:
            async with session.begin():
                res = await session.execute(increment_like)
                if res.rowcount == 0:  # no like
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Incorrect post_id",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                res = await session.execute(add_to_like_table)
                if res.rowcount == 0:  # no like
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Incorrect post_id",
                        headers={"WWW-Authenticate": "Bearer"},
                    )

                await session.commit()

    async def delete_like(self, post_id, user_id):
        decrement_like_counter = (
            update(Post)
            .values(likes=Post.likes - 1)
            .where(
                (Post.id == post_id)
                & (Post.likes > 0)
                & (
                    Post.id.in_(
                        select(Like.post_id).where(
                            (Like.user_id == user_id) & (Like.post_id == post_id)
                        )
                    )
                )
            )
        )

        delete_like = delete(Like).where(
            (Like.post_id == post_id) & (Like.user_id == user_id)
        )

        async_session = await get_session()

        async with async_session() as session:
            async with session.begin():
                res = await session.execute(decrement_like_counter)
                if res.rowcount == 0:  # no like
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Incorrect post_id",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                res = await session.execute(delete_like)
                if res.rowcount == 0:  # no like
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Incorrect post_id",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                await session.commit()
