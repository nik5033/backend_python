import os
from dotenv import load_dotenv

load_dotenv()


class PostgresConfig:
    url = "postgres+psycopg2://{user}:{password}@{host}:{port}/{name}".format(
        user=os.getenv('POSTGRES_USER', "postgres"),
        password=os.getenv('POSTGRES_PASSWORD', 'postgres'),
        host=os.getenv('POSTGRES_HOST', 'localhost'),
        port=int(os.getenv('POSTGRES_PORT', 5432)),
        name=os.getenv('POSTGRES_NAME', 'messenger')
    )
