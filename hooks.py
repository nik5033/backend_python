from sqlalchemy import create_engine

from configs.config import ApplicationConfig
from context import Context
from database.database import Database


def init_db_postgres(config: ApplicationConfig, context: Context):
    engine = create_engine(
        config.database.url,
        pool_pre_ping=True,
    )

    database = Database(connection=engine)
    database.check()

    context.set('database', database)