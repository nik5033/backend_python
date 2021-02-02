from api.request.create_user import ReqCreateUserDTO
from api.request.update_user import ReqUpdateUserDTO
from database.database import DBSession
from database.exceptions import DBUserNotExistsException, DBUserExistsException
from database.models.user import UserModel


def create_user(session: DBSession, user: ReqCreateUserDTO, password: str) -> UserModel:
    if session.get_user_by_username(user.username) is not None:
        raise DBUserExistsException

    new_user = UserModel(
        username=user.username,
        password=password,
        first_name=user.first_name,
        last_name=user.last_name,
    )

    session.add_model(new_user)

    return new_user


def get_user(session: DBSession, *, username: str = None, user_id: int = None) -> UserModel:
    db_employee = None

    if username is not None:
        db_employee = session.get_user_by_username(username)
    elif user_id is not None:
        db_employee = session.get_user_by_id(user_id)

    if db_employee is None or db_employee.is_delete is True:
        raise DBUserNotExistsException
    return db_employee


def update_user(session: DBSession, uid: int, user: ReqUpdateUserDTO) -> UserModel:
    db_user = session.get_user_by_id(uid)

    for attr in user.fields:
        if hasattr(user, attr):
            setattr(db_user, attr, getattr(user, attr))

    return db_user


def full_delete_user(session: DBSession, uid: int):
    db_user = session.get_user_by_id(uid)

    if db_user is None:
        raise DBUserNotExistsException

    session.delete(db_user)


def delete_user(session: DBSession, uid: int):
    db_user = session.get_user_by_id(uid)

    if db_user is None:
        raise DBUserNotExistsException

    db_user.is_delete = True
