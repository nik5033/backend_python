from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request.update_msg import ReqUpdateMsgDTO
from api.response.get_msg import ResGetMsgDTO
from database.database import DBSession
from database.exceptions import DBMsgNotExistsException, DBIntegrityException, DBDataException
from database.queries import message as msg_queries
from transport.sanic.endpoint import BaseEndpoint
from transport.sanic.exceptions import SanicMsgNotFoundException, SanicDBException


class ChangeMsgEndpoint(BaseEndpoint):

    async def method_patch(self, request: Request, body: dict, session: DBSession, msg_id: int, token: dict, *args, **kwargs) -> BaseHTTPResponse:

        try:
            db_msg = session.get_msg_by_id(msg_id)
        except DBMsgNotExistsException:
            raise SanicMsgNotFoundException

        if token.get('uid') is not db_msg.sender_id:
            return await self.make_response_json(status=403)

        req_model = ReqUpdateMsgDTO(body)

        try:
            db_msg = msg_queries.update_msg(session, db_msg.id, req_model)
        except DBMsgNotExistsException:
            raise SanicMsgNotFoundException

        try:
            session.commit()
        except (DBIntegrityException, DBDataException):
            raise SanicDBException

        res_model = ResGetMsgDTO(db_msg)

        return await self.make_response_json(body=res_model.dump(), status=200)

    async def method_get(self, request: Request, body: dict, session: DBSession, msg_id: int, token: dict, *args, **kwargs):
        try:
            db_msg = msg_queries.get_msg(session, msg_id)
        except DBMsgNotExistsException:
            raise SanicMsgNotFoundException("Message not found")

        if token.get('uid') is not db_msg.sender_id and token.get('uid') is not db_msg.recipient_id:
            return await self.make_response_json(status=403)

        res_model = ResGetMsgDTO(db_msg)

        return await self.make_response_json(body=res_model.dump(), status=200)

    async def method_delete(self, request: Request, body: dict, session: DBSession, msg_id: int, token: dict, *args, **kwargs):
        try:
            db_msg = msg_queries.get_msg(session, msg_id)
        except DBMsgNotExistsException:
            raise SanicMsgNotFoundException("Message not found")

        if token.get('uid') is not db_msg.sender_id:
            return await self.make_response_json(status=403)

        msg_queries.delete_msg(session, msg_id)

        try:
            session.commit()
        except (DBIntegrityException, DBDataException):
            raise SanicDBException

        return await self.make_response_json(body={}, status=200)