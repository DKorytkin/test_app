
from aiohttp import web

from test_app.handlers.user import users, create_user
from test_app.handlers.order import get_orders
from test_app.handlers.main import main


def setup_routes(app: web.Application):

    app.router.add_get(
        path='/',
        handler=main
    )

    # Users
    app.router.add_get(
        path='/users',
        handler=users
    )
    app.router.add_post(
        path='/users',
        handler=create_user
    )
    app.router.add_get(
        path='/users/{user_id}',
        handler=users
    )

    # Orders
    app.router.add_get(
        path='/users/{user_id}/orders',
        handler=get_orders
    )
    app.router.add_get(
        path='/users/{user_id}/orders/{order_id}',
        handler=get_orders
    )
