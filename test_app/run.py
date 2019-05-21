
import logging
import os

from aiohttp import web
from aiopg.sa import create_engine

from test_app.routes import setup_routes


log = logging.getLogger(__name__)


async def db_ctx(app):
    app.db = await create_engine(
        user=os.getenv('POSTGRES_USER'),
        database=os.getenv('POSTGRES_DB'),
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT'),
        password=os.getenv('POSTGRES_PASSWORD'),
    )
    yield
    app.db.close()
    await app.db.wait_closed()


def init(loop=None) -> web.Application:
    # loop only for tests
    app = web.Application()
    setup_routes(app)
    app.cleanup_ctx.append(db_ctx)
    return app


if __name__ == '__main__':
    web.run_app(init())
