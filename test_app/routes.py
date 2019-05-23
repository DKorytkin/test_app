
from aiohttp import web

from test_app.handlers.user import users, create_user
from test_app.handlers.order import get_order, get_orders, create_order
from test_app.handlers.product import get_products, create_product
from test_app.handlers.main import main


def setup_routes(app: web.Application):
    # Health
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
    app.router.add_post(
        path='/orders',
        handler=create_order
    )
    app.router.add_get(
        path='/users/{user_id}/orders',
        handler=get_orders
    )
    app.router.add_get(
        path='/users/{user_id}/orders/{order_id}',
        handler=get_order
    )

    # Products
    app.router.add_get(
        path='/products',
        handler=get_products
    )
    app.router.add_post(
        path='/products',
        handler=create_product
    )
    app.router.add_get(
        path='/products/{product_id}',
        handler=get_products
    )
