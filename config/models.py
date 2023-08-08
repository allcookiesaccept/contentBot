from dataclasses import dataclass

@dataclass
class BotApi:
    token: str


@dataclass
class Postgres:
    host: str
    port: str
    database: str
    user: str
    password: str