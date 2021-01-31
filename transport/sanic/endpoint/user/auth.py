from sanic.request import Request
from sanic.response import BaseHTTPResponse

from transport.sanic.endpoint import BaseEndpoint
from transport.sanic.exceptions import SanicUserNotFound, SanicPassHashException

from api.request.auth import ReqAuthDTO

from database.queries import user as user_queries
from database.exceptions import DBUserNotExistsException

from helpers.password.password import check_pass
from helpers.auth.token import create_token
from helpers.password.exceptions import CheckPassHashException


class AuthUserEndpoint(BaseEndpoint):

    async def method_post(self, request: Request, body: dict, session, *args, **kwargs) -> BaseHTTPResponse:

        request_model = ReqAuthDTO(body)
        status = 401
        res_body = {}

        try:
            db_user = user_queries.get_user(session, username=request_model.username)
        except DBUserNotExistsException:
            raise SanicUserNotFound("User not found")

        try:
            if check_pass(request_model.password, db_user.password):
                status = 200
                payload = {
                    'uid': db_user.id,
                }
                res_body = {
                    "Authorization": create_token(payload)
                }

        except CheckPassHashException:
            raise SanicPassHashException("Wrong password")

        return await self.make_response_json(body=res_body, status=status)


