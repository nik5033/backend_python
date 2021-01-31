from transport.sanic.config import SanicConfig
from database.config import PostgresConfig


class ApplicationConfig:
    sanic: SanicConfig
    database: PostgresConfig

    def __init__(self):
        self.sanic = SanicConfig()
        self.database = PostgresConfig()