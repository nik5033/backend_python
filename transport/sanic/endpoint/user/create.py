from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.response.get_user import ResGetUserDTO
from database.database import DBSession
from database.exceptions import DBIntegrityException, DBDataException, DBUserExistsException
from transport.sanic.endpoint import BaseEndpoint
from api.request import ReqCreateUserDTO
from helpers.password import generate_hash
from database.queries import user as user_query
from transport.sanic.exceptions import SanicDBException, SanicUserConflictException


class CreateUserEndpoint(BaseEndpoint):

    async def method_post(self, request: Request, body: dict, session: DBSession, *args, **kwargs) -> BaseHTTPResponse:
        req_model = ReqCreateUserDTO(body)

        hash_pass = generate_hash(req_model.password)
        try:
            db_user = user_query.create_user(session, req_model, hash_pass)
        except DBUserExistsException:
            raise SanicUserConflictException("User already exist")
        try:
            session.commit()
        except (DBIntegrityException, DBDataException):
            raise SanicDBException

        response_model = ResGetUserDTO(db_user)

        return await self.make_response_json(body=response_model.dump(), status=201)
