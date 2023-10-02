from dotenv import load_dotenv
import os
from .models import Postgres, TelegramBot, BotConfig

class DataManager:
    __instance = None
    @staticmethod
    def get_instance():
        if DataManager.__instance is None:
            DataManager()
        return DataManager.__instance

    def __init__(self):
        if DataManager.__instance is not None:
            raise Exception("DataManger is a singleton class")
        else:
            load_dotenv()
            self.bot = self.get_token()
            self.postgres = self.load_postgres_data()
            DataManager.__instance = self

    def get_token(self) -> BotConfig:

        token = os.getenv("TOKEN")
        tg_bot: TelegramBot = TelegramBot(token=token)
        return BotConfig(tg_bot=tg_bot)

    def load_postgres_data(self) -> Postgres:

        host = os.getenv("POSTGRES_HOST")
        port = os.getenv("POSTGRES_PORT")
        database = os.getenv("POSTGRES_DB")
        user = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_PASSWORD")

        return Postgres(host, port, database, user, password)
