import asyncio
import logging

from aiogram import Bot, Dispatcher

from config.data_manager import DataManager
from config.models import BotConfig
from handlers import user


logger = logging.getLogger(__name__)

# TODO fix "AttributeError: 'NoneType' object has no attribute 'dataframe'" for DescriptionMatcher


def logger_setup():
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )

    logger.info("Starting bot")


async def main():
    logger_setup()
    data_manager: DataManager = DataManager.get_instance()

    config: BotConfig = data_manager._DataManager__bot_token

    bot: Bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp: Dispatcher = Dispatcher(bot=bot)

    dp.include_router(user.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
