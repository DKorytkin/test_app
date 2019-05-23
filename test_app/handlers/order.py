import trafaret as t
from trafaret.dataerror import DataError
from aiohttp import web
from sqlalchemy import select

from test_app.models.db import carts, orders, products
from test_app.handlers.schemas.order import ORDER_ADD


async def get_orders(request):
    user_id = request.match_info.get('user_id')
    query = (
        select([orders.c.id])
        .where(orders.c.account_id == user_id)
        .order_by(orders.c.id)
    )
    data = []
    async with request.app.db.acquire() as connection:
        async for line in connection.execute(query):
            data.append({'id': line.id})
    return web.json_response({'success': True, 'data': data})


async def get_order(request):
    user_id = request.match_info.get('user_id')
    order_id = request.match_info.get('order_id')

    query = (
        select([orders])
        .where(orders.c.account_id == user_id)
        .where(orders.c.id == order_id)
    )
    async with request.app.db.acquire() as connection:
        result = await connection.execute(query)
        order = await result.first()

    query = (
        select([carts, products], use_labels=True)
        .select_from(
            carts.join(products, carts.c.product_id == products.c.id)
        )
        .where(carts.c.order_id == order.id)
        .order_by(carts.c.order_id)
    )

    order_info = {
        'id': order.id,
        'account_id': order.account_id,
        'date_created': str(order.date_created),
        'date_edited': str(order.date_edited),
    }
    data = []
    async with request.app.db.acquire() as connection:
        async for line in connection.execute(query):
            data.append({
                'id': line.products_id,
                'name': line.products_name,
                'price': line.products_price
            })

    order_info.update({'products': data})
    return web.json_response({'success': True, 'data': order_info})


async def create_order(request):
    try:
        data = await request.post()
        info = ORDER_ADD.check({
            'user_id': data.get('user_id'),
            'product_ids': data.getall('product_ids')
        })
    except t.dataerror.DataError as e:
        return web.json_response({'success': False, 'error': e.as_dict()})

    async with request.app.db.acquire() as connection:
        result = await connection.execute(orders.insert().values(**{
            'account_id': info['user_id']
        }))
        order = await result.first()
        for product_id in info['product_ids']:
            await connection.execute(carts.insert().values(**{
                'order_id': order.id,
                'product_id': product_id
            }))

    return web.json_response({'success': True, 'data': {'id': order.id}})
