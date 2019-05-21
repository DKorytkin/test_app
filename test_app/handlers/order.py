import trafaret as t
from aiohttp import web
from sqlalchemy import select

from test_app.models.db import accounts, orders


async def get_orders(request):
    user_id = request.match_info.get('user_id')
    order_id = request.match_info.get('order_id')
    query = (
        select([accounts, orders], use_labels=True)
        .select_from(
            accounts.join(orders, accounts.c.id == orders.c.account_id),
        )
        .where(accounts.c.id == user_id)
        .order_by(orders.c.id)
    )
    if order_id:
        query = query.where(orders.c.id == order_id)

    data = []
    async with request.app.db.acquire() as connection:
        async for line in connection.execute(query):
            info = {'id': line.orders_id}
            if order_id:
                info.update({
                    'account_id': line.accounts_id,
                    'date_created': str(line.orders_date_created),
                    'date_edited': str(line.orders_date_edited),
                })
            data.append(info)
    return web.json_response({'success': True, 'data': data})


async def create_order(request):
    user_id = request.match_info.get('user_id')
    try:

        info = t.Int().check(user_id)
    except t.dataerror.DataError as e:
        return web.json_response({'success': False, 'error': e.as_dict()})

    async with request.app.db.acquire() as connection:
        result = await connection.execute(accounts.insert().values(**{'account_id': info}))
        user = await result.first()

    return web.json_response({'success': True, 'data': {'id': user.id}})
