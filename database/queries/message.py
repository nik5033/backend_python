from typing import List

from api.request.send_msg import ReqCreateMsgDTO
from api.request.update_msg import ReqUpdateMsgDTO
from database.database import DBSession
from database.exceptions import DBUserNotExistsException, DBMsgNotExistsException
from database.models.message import MessageModel
from database.queries.user import get_user


def create_msg(session: DBSession, message: ReqCreateMsgDTO, sender_id: int) -> MessageModel:
    recip = get_user(session, username=message.recipient)

    if recip is None or recip.is_delete is True:
        raise DBUserNotExistsException

    new_msg = MessageModel(
        message=message.message,
        sender_id=sender_id,
        recipient_id=recip.id,
    )

    session.add_model(new_msg)

    return new_msg


def get_msgs(session: DBSession, uid: int) -> List[MessageModel]:
    return session.get_msg_all(uid)


def get_msg(session: DBSession, msg_id: int) -> MessageModel:
    db_msg = session.get_msg_by_id(msg_id)

    if db_msg is None or db_msg.is_delete is True:
        raise DBMsgNotExistsException
    return db_msg


def update_msg(session: DBSession, msg_id: int, message: ReqUpdateMsgDTO) -> MessageModel:
    db_msg = session.get_msg_by_id(msg_id)

    if db_msg is None or db_msg.is_delete is True:
        raise DBMsgNotExistsException

    db_msg.message = message.message

    return db_msg


def full_delete_msg(session: DBSession, msg_id: int):
    db_msg = session.get_msg_by_id(msg_id)
    if db_msg is None or db_msg.is_delete is True:
        raise DBMsgNotExistsException
    session.delete(db_msg)


def delete_msg(session: DBSession, msg_id: int):
    db_msg = session.get_msg_by_id(msg_id)

    if db_msg is None or db_msg.is_delete is True:
        raise DBMsgNotExistsException

    db_msg.is_delete = True


def delete_msgs(session: DBSession):
    pass
