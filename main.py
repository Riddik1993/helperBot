import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from configuration import Configuration
from configuration.Configuration import load_config
from database.models.base import Base
from handlers import user_handlers, admin_handlers
from middlewares.DbSessionMiddleware import DbSessionMiddleware
from middlewares.TrackAllUsersMiddleware import TrackAllUsersMiddleware


async def main():
    config: Configuration = load_config()

    bot = Bot(token=config.telegram.token)
    dp = Dispatcher()
    dp.include_router(user_handlers.router)
    dp.include_router(admin_handlers.router)
    dp.workflow_data.update(config=config)

    engine = create_async_engine(url=config.db.dsn, echo=config.db.echo)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    Sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    dp.update.outer_middleware(DbSessionMiddleware(Sessionmaker))
    dp.message.outer_middleware(TrackAllUsersMiddleware())

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
