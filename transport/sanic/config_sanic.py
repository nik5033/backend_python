from sanic import Sanic

from configs.config import ApplicationConfig
from context import Context
from transport.sanic.routes import get_routes
from hooks import init_db_postgres


def config_app(config: ApplicationConfig, context: Context) -> Sanic:
    app = Sanic(__name__)
    init_db_postgres(config, context)

    for handler in get_routes(config, context):
        app.add_route(
            handler=handler,
            uri=handler.uri,
            methods=handler.methods,
            strict_slashes=True,
        )

    return app
