from dotenv import load_dotenv
import os
from .models import BotApi, Postgres



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
            self.__bitrix_user = self.load_bitrix_user()
            self.__postgres_info = self.load_postgres_data()
            DataManager.__instance = self

    def get_token(self) -> BotApi:

        token = os.getenv("TOKEN")
        return BotApi(token)

    def load_postgres_data(self) -> Postgres:

        host = os.getenv("POSTGRES_HOST")
        port = os.getenv("POSTGRES_PORT")
        database = os.getenv("POSTGRES_DB")
        user = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_PASSWORD")

        return Postgres(host, port, database, user, password)
