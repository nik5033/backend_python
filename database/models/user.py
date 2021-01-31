from sqlalchemy import Column, VARCHAR, BOOLEAN, LargeBinary

from database.models import BaseModel


class UserModel(BaseModel):

    __tablename__ = 'users'

    username = Column(
        VARCHAR(100),
        nullable=False,
        unique=True,
    )

    password = Column(
        VARCHAR(200),
        nullable=False,
    )

    first_name = Column(
        VARCHAR(50),
    )
    last_name = Column(
        VARCHAR(50),
    )

    is_delete = Column(
        BOOLEAN,
        nullable=False,
        default=False
    )


