from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request.update_user import ReqUpdateUserDTO
from api.response.get_user import ResGetUserDTO
from database.database import DBSession
from database.exceptions import DBUserNotExistsException, DBIntegrityException, DBDataException
from database.queries import user as user_queries
from database.queries import message as msg_queries
from transport.sanic.endpoint import BaseEndpoint
from transport.sanic.exceptions import SanicUserNotFoundException, SanicDBException, SanicAuthException


class UserEndpoint(BaseEndpoint):

    async def method_get(self, request: Request, body: dict, session: DBSession, uid: int, token: dict, *args, **kwargs) -> BaseHTTPResponse:

        if token.get('uid') != uid:
            return await self.make_response_json(status=403)
        try:
            db_user = user_queries.get_user(session, user_id=uid)
        except DBUserNotExistsException:
            raise SanicAuthException("Unauthorized")

        res_model = ResGetUserDTO(db_user)

        return await self.make_response_json(body=res_model.dump(), status=200)

    async def method_patch(self, request: Request, body: dict, session: DBSession, uid: int, token: dict, *args, **kwargs) -> BaseHTTPResponse:
        if token.get('uid') != uid:
            return await self.make_response_json(status=403)

        req_model = ReqUpdateUserDTO(body)

        try:
            user = user_queries.update_user(session, uid, req_model)
        except DBUserNotExistsException:
            raise SanicUserNotFoundException("User not found")

        try:
            session.commit()
        except (DBIntegrityException, DBDataException):
            raise SanicDBException

        res_model = ResGetUserDTO(user)

        return await self.make_response_json(body=res_model.dump(), status=200)

    async def method_delete(self, request: Request, body: dict, session: DBSession, uid: int, token: str, *args, **kwargs) -> BaseHTTPResponse:
        if token.get('uid') != uid:
            return await self.make_response_json(status=403)

        try:
            user_queries.delete_user(session, uid)
        except DBUserNotExistsException:
            raise SanicUserNotFoundException("User not found")

        msgs = msg_queries.get_msgs(session, uid)

        for msg in msgs:
            try:
                user = user_queries.get_user(session, user_id=msg.recipient_id)
            except DBUserNotExistsException:
                user = None
            if uid is msg.sender_id and user is None:
                msg.is_delete = True
            try:
                user = user_queries.get_user(session, user_id=msg.sender_id)
            except DBUserNotExistsException:
                user = None
            if uid is msg.recipient_id and user is None:
                msg.is_delete = True

        try:
            session.commit()
        except (DBIntegrityException, DBDataException):
            raise SanicDBException

        return await self.make_response_json(body={}, status=200)