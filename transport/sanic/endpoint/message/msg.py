from sanic.request import Request
from sanic.response import BaseHTTPResponse

from database.database import DBSession
from database.exceptions import DBUserNotExistsException, DBIntegrityException, DBDataException
from database.queries import message as message_queries
from transport.sanic.endpoint import BaseEndpoint
from api.request.send_msg import ReqCreateMsgDTO
from api.response.get_msg import ResGetMsgDTO
from api.response.get_all_msgs import ResGetAllMsgDTO
from transport.sanic.exceptions import SanicDBException, SanicUserNotFoundException


class MsgEndpoint(BaseEndpoint):

    async def method_post(self, request: Request, body: dict, session: DBSession, token: dict, *args,
                          **kwargs) -> BaseHTTPResponse:

        req_model = ReqCreateMsgDTO(body)

        try:
            db_msg = message_queries.create_msg(session, req_model, token.get('uid'))
        except DBUserNotExistsException:
            raise SanicUserNotFoundException("User not found")

        try:
            session.commit()
        except (DBIntegrityException, DBDataException):
            raise SanicDBException

        res_model = ResGetMsgDTO(db_msg)

        return await self.make_response_json(body=res_model.dump(), status=201)

    async def method_get(self, request: Request, body: dict, session: DBSession, token: dict, *args,
                         **kwargs) -> BaseHTTPResponse:
        db_messages = message_queries.get_msgs(session, token.get('uid'))

        res_model = ResGetAllMsgDTO(db_messages, many=True)

        return await self.make_response_json(body=res_model.dump(), status=200)
