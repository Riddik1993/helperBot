from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from configuration.Configuration import DatabaseConfig
from database.models.base import Base


async def get_db_session_maker(dbConfig: DatabaseConfig):
    engine = create_async_engine(url=dbConfig.dsn, echo=dbConfig.echo)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    return async_sessionmaker(engine, expire_on_commit=False)
