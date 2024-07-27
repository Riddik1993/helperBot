import asyncio
from aiogram import Bot, Dispatcher
from configuration import Configuration
from configuration.Configuration import load_config
from handlers import user_handlers, admin_handlers


async def main() -> None:
    config: Configuration = load_config()

    bot = Bot(token=config.telegram.token)
    dp = Dispatcher()

    dp.include_router(user_handlers.router)
    dp.include_router(admin_handlers.router)
    dp.workflow_data.update(config=config)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, config=config)


if __name__ == '__main__':
    asyncio.run(main())
