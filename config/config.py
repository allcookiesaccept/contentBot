from dataclasses import dataclass
from dotenv import load_dotenv
from .helpers import get_env_variable


@dataclass
class TelegramBot:
    token: str


@dataclass
class Config:
    tg_bot: TelegramBot


def load_config() -> Config:
    load_dotenv()

    tg_bot: TelegramBot = TelegramBot(token=get_env_variable("BOT_TOKEN"))
    return Config(tg_bot=tg_bot)
