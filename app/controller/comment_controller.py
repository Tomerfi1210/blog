from app.controller.blog_controller import BlogController
from app.db import get_session
from app.tables import Comment
from fastapi import HTTPException, status
from sqlalchemy import insert, delete


class CommentController(BlogController):
    async def add_comment(self, post_id, user_id, comment: str):
        add_to_comment_table = insert(Comment).values(
            post_id=post_id, user_id=user_id, comment=comment
        )

        async_session = await get_session()

        async with async_session() as session:
            async with session.begin():
                res = await session.execute(add_to_comment_table)
                if res.rowcount == 0:  # no comment
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Incorrect post_id",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                await session.commit()

        return res.inserted_primary_key[0]

    async def delete_comment(self, comment_id, post_id, user_id):
        delete_comment_query = delete(Comment).where(
            (Comment.id == comment_id)
            & (Comment.post_id == post_id)
            & (Comment.user_id == user_id)
        )

        async_session = await get_session()

        async with async_session() as session:
            async with session.begin():
                res = await session.execute(delete_comment_query)
                if res.rowcount == 0:  # no comment
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Comment not found",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                await session.commit()
