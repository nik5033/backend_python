from typing import Tuple

from configs.config import ApplicationConfig
from context import Context
from transport.sanic import endpoint
from transport.sanic.base import SanicEndpoint


def get_routes(config: ApplicationConfig, context: Context) -> Tuple[SanicEndpoint, ...]:
    return (
        endpoint.CreateUserEndpoint(
            config=config, context=context, uri='/user', methods=('POST',)
        ),
        endpoint.AuthUserEndpoint(
            config=config, context=context, uri='/auth', methods=('POST',)
        ),
        endpoint.UserEndpoint(
            config=config, context=context, uri='/user/<uid:int>', methods=('GET', 'PATCH', 'DELETE'), auth=True
        ),
        endpoint.MsgEndpoint(
            config=config, context=context, uri='/msg', methods=('POST', 'GET',), auth=True
        ),
        endpoint.ChangeMsgEndpoint(
            config=config, context=context, uri='/msg/<msg_id:int>', methods=('GET', 'PATCH', 'DELETE'), auth=True
        ),
    )
