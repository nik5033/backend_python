from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request.update_user import ReqUpdateUserDTO
from api.response.get_user import ResGetUserDTO
from database.database import DBSession
from database.exceptions import DBUserNotExistsException, DBIntegrityException, DBDataException
from database.queries import user as user_query
from transport.sanic.endpoint import BaseEndpoint
from transport.sanic.exceptions import SanicUserNotFound, SanicDBException


class UserEndpoint(BaseEndpoint):

    async def method_get(self, request: Request, body: dict, session: DBSession, uid: int, token: dict, *args, **kwargs) -> BaseHTTPResponse:

        if token.get('uid') != uid:
            return await self.make_response_json(status=403)
        db_user = user_query.get_user(session, user_id=uid)

        res_model = ResGetUserDTO(db_user)

        return await self.make_response_json(body=res_model.dump(), status=200)

    async def method_patch(self, request: Request, body: dict, session: DBSession, uid: int, token: dict, *args, **kwargs):
        if token.get('uid') != uid:
            return await self.make_response_json(status=403)

        req_model = ReqUpdateUserDTO(body)

        try:
            user = user_query.update_user(session, uid, req_model)
        except DBUserNotExistsException:
            raise SanicUserNotFound("User not found")

        try:
            session.commit()
        except (DBIntegrityException, DBDataException):
            raise SanicDBException

        res_model = ResGetUserDTO(user)

        return await self.make_response_json(body=res_model.dump(), status=200)
