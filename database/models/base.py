import datetime

from sqlalchemy import Column, Integer, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base


class BaseModel(declarative_base()):

    __abstract__ = True

    id = Column(
        Integer,
        nullable=False,
        autoincrement=True,
        unique=True,
        primary_key=True,
    )

    created_at = Column(
        TIMESTAMP,
        nullable=False,
        default=datetime.datetime.utcnow,
    )

    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )