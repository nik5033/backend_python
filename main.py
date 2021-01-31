from configs.config import ApplicationConfig
from context import Context
from transport.sanic.config_sanic import config_app


def main():
    config = ApplicationConfig()
    context = Context()
    app = config_app(config, context)

    app.run(
        host=config.sanic.host,
        port=config.sanic.port,
        workers=config.sanic.workers,
        debug=config.sanic.debug,
    )


if __name__ == '__main__':
    main()
