from dotenv import load_dotenv
import os
from .models import TelegramBot, BotConfig

class DataManager:
    __instance = None

    @staticmethod
    def get_instance():
        if DataManager.__instance is None:
            DataManager()
        return DataManager.__instance

    def __init__(self):
        if DataManager.__instance is not None:
            raise Exception("DataManager is a singleton class")
        else:
            load_dotenv()
            self.bot = self.get_token()
            DataManager.__instance = self

    def get_token(self) -> BotConfig:
        token = os.getenv("TOKEN")
        return BotConfig(tg_bot=TelegramBot(token=token))