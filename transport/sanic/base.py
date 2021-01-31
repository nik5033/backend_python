from http import HTTPStatus
from typing import Iterable

from sanic.request import Request
from sanic.response import BaseHTTPResponse, json

from configs.config import ApplicationConfig
from context import Context
from helpers.auth.exceptions import ReadTokenException
from helpers.auth.token import read_token
from transport.sanic.exceptions import SanicAuthException


class SanicEndpoint:

    async def __call__(self, request: Request, *args, **kwargs) -> BaseHTTPResponse:
        if self.auth:
            try:
                token = {
                    'token': self.import_body_auth(request),
                }
            except SanicAuthException as e:
                return await self.make_response_json(status=e.status_code)
            else:
                kwargs.update(token)

        return await self.handler(request, *args, **kwargs)

    def __init__(
            self,
            config: ApplicationConfig,
            context: Context,
            uri: str,
            methods: Iterable,
            auth: bool = False,
            *args,
            **kwargs):
        self.config = config
        self.context = context
        self.uri = uri
        self.methods = methods
        self.auth = auth

    @staticmethod
    def import_body_json(request: Request) -> dict:
        if 'application/json' in request.content_type and request.json is not None:
            return dict(request.json)
        return {}

    @staticmethod
    def import_body_headers(request: Request) -> dict:
        return {
            header: value
            for header, value in request.headers.items()
            if header.lower().startswith('x-')
        }

    @staticmethod
    def import_body_auth(request: Request) -> dict:
        token = request.headers.get('Authorization')
        try:
            return read_token(token)
        except ReadTokenException as e:
            raise SanicAuthException(str(e))

    @staticmethod
    async def make_response_json(
            body: dict = None, status: int = 400, message: str = None, error: int = None
    ) -> BaseHTTPResponse:
        if body is None:
            res_body = {
                'message': message or HTTPStatus(status).phrase,
                'error': error or status,
            }
            return json(body=res_body, status=status)
        return json(body=body, status=status)

    async def handler(self, request: Request, *args, **kwargs) -> BaseHTTPResponse:
        body = {}

        body.update(self.import_body_json(request))
        body.update(self.import_body_headers(request))

        return await self._methods(request, body, *args, **kwargs)

    async def _methods(self, request: Request, body: dict, *args, **kwargs) -> BaseHTTPResponse:
        method = request.method.lower()
        function_name = f'method_{method}'

        if hasattr(self, function_name):
            func = getattr(self, function_name)
            return await func(request, body, *args, **kwargs)
        return await self.method_not_exist(method=method)

    async def method_not_exist(self, method: str) -> BaseHTTPResponse:
        return await self.make_response_json(status=501, message=f'Method {method.upper()} does not exist')

    async def method_get(self, request: Request, body: dict, *args, **kwargs):
        return await self.method_not_exist('GET')

    async def method_post(self, request: Request, body: dict, *args, **kwargs):
        return await self.method_not_exist('POST')

    async def method_patch(self, request: Request, body: dict, *args, **kwargs):
        return await self.method_not_exist('PATCH')

    async def method_delete(self, request: Request, body: dict, *args, **kwargs):
        return await self.method_not_exist('DELETE')
