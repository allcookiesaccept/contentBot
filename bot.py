import asyncio
from aiogram import Bot, Dispatcher
from config.data_manager import DataManager
from config.models import BotConfig
from handlers.user import BotRouter
from config.logger import logger



async def main():

    logger.info("Starting bot")
    data_manager: DataManager = DataManager.get_instance()

    config: BotConfig = data_manager.bot

    bot: Bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp: Dispatcher = Dispatcher(bot=bot)

    # dp.include_router(user.router)
    user_router = BotRouter(dp=dp)
    dp.include_router(user_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
