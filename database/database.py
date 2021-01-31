from typing import List

from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm import Session, sessionmaker, Query

from database.exceptions import DBIntegrityException, DBDataException
from database.models import BaseModel, UserModel
from database.models.message import MessageModel


class DBSession:
    _session: Session

    def __init__(self, session: Session):
        self._session = session

    def query(self, *args, **kwargs) -> Query:
        return self._session.query(*args, **kwargs)

    def add_model(self, model: BaseModel):
        try:
            self._session.add(model)
        except IntegrityError as err:
            raise DBIntegrityException(err)
        except DataError as err:
            raise DBDataException(err)

    def get_user_by_username(self, username: str) -> UserModel:
        return self.query(UserModel).filter(UserModel.username == username).first()

    def get_user_by_id(self, uid: int) -> UserModel:
        return self.query(UserModel).filter(UserModel.id == uid).first()

    def get_user_all(self) -> List[UserModel]:
        return self.query(UserModel).filter(UserModel.is_delete == 0).all()

    def get_msg_by_id(self, m_id: int) -> MessageModel:
        return self.query(MessageModel).filter(MessageModel.id == m_id).first()

    def get_msg_all(self, uid: int) -> List[MessageModel]:
        msgs1 = self.query(MessageModel).filter(uid == MessageModel.sender_id).all()
        msgs2 = self.query(MessageModel).filter(uid == MessageModel.recipient_id).all()
        return list(set(msgs1) | set(msgs2))

    def delete(self, model: BaseModel):
        self._session.delete(model)

    def commit(self, need_close: bool = False):
        try:
            self._session.commit()
        except IntegrityError as err:
            raise DBIntegrityException(err)
        except DataError as err:
            raise DBDataException(err)

        if need_close:
            self._session.close()


class Database:
    connection: Engine
    session_maker: sessionmaker
    _test = 'SELECT 1'

    def __init__(self, connection: Engine):
        self.connection = connection
        self.session_maker = sessionmaker(bind=self.connection)

    def check(self):
        self.connection.execute(self._test).fetchone()

    def make_session(self) -> DBSession:
        return DBSession(self.session_maker())
