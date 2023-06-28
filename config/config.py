import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field
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
