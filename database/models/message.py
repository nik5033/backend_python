from sqlalchemy import Column, VARCHAR, Integer, BOOLEAN

from database.models import BaseModel


class MessageModel(BaseModel):

    __tablename__ = 'messages'

    sender_id = Column(
        Integer,
        nullable=False,
    )

    recipient_id = Column(
        Integer,
        nullable=False,
    )

    message = Column(
        VARCHAR(500),
        nullable=False,
    )

    is_delete = Column(
        BOOLEAN,
        nullable=False,
        default=False
    )
