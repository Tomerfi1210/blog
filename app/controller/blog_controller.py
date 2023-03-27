from app.db import get_session
from app.schema.model import SignUpSchema
from app.tables import User
from app.auth.auth import get_password_hash
from abc import ABC


class BlogController(ABC):
    async def signup_user(self, signup_schema: SignUpSchema) -> None:
        user = User(
            username=signup_schema.username,
            password=get_password_hash(signup_schema.password),
            email=signup_schema.email,
            full_name=signup_schema.full_name,
        )

        async_session = await get_session()

        async with async_session() as session:
            async with session.begin():
                session.add(user)
                await session.commit()
