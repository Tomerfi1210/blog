from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()


async def get_session():
    engine = create_async_engine(
        f"postgresql+asyncpg://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}:5432/{os.environ['POSTGRES_DB']}",
        echo=True,
    )

    async_session = async_sessionmaker(engine, expire_on_commit=False)
    return async_session
