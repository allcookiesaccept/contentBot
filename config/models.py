from dataclasses import dataclass
import pandas

@dataclass
class TelegramBot:
    token: str

@dataclass
class BotConfig:
    tg_bot: TelegramBot

@dataclass()
class CSVFile:
    filename: str
    dataframe: pandas.DataFrame
    type: str
