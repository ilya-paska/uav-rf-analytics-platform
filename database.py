import psycopg2
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import DB_PASSWORD


DATABASE_URL = f"postgresql+asyncpg://postgres:{DB_PASSWORD}@127.0.0.1:5432/postgres"


engine = create_async_engine(DATABASE_URL, echo=False, future=True)

async_session = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)


async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
