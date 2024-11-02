import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from configuration import Configuration
from configuration.Configuration import load_config
from database.session import get_db_session_maker
from handlers import user_handlers, admin_handlers
from keyboards.menu_button import set_main_menu
from middlewares.DbSessionMiddleware import DbSessionMiddleware
from middlewares.TrackAllUsersMiddleware import TrackAllUsersMiddleware

config: Configuration = load_config()


async def main():
    bot = Bot(
        token=config.telegram.token, default=DefaultBotProperties(parse_mode="HTML")
    )
    dp = Dispatcher()
    dp.include_router(user_handlers.router)
    dp.include_router(admin_handlers.router)
    dp.workflow_data.update(config=config)
    dp.startup.register(set_main_menu)

    db_sessionmaker = await get_db_session_maker(config.db)
    dp.update.outer_middleware(DbSessionMiddleware(db_sessionmaker))
    dp.message.outer_middleware(TrackAllUsersMiddleware())

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
