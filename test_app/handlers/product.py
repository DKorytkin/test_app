import trafaret as t
from trafaret.dataerror import DataError
from aiohttp import web
from sqlalchemy import select

from test_app.models.db import products
from test_app.handlers.schemas.product import PRODUCT_ADD


async def get_products(request):
    product_id = request.match_info.get('product_id')
    query = select([products]).order_by(products.c.id)
    if product_id:
        query = query.where(products.c.id == product_id)

    data = []
    async with request.app.db.acquire() as connection:
        async for line in connection.execute(query):
            info = {'id': line.id}
            if product_id:
                info.update({
                    'name': line.name,
                    'price': line.price,
                    'date_created': str(line.date_created),
                    'date_edited': str(line.date_edited),
                })
            data.append(info)
    return web.json_response({'success': True, 'data': data})


async def create_product(request):
    try:
        info = PRODUCT_ADD.check(await request.post())
    except t.dataerror.DataError as e:
        return web.json_response({'success': False, 'error': e.as_dict()})

    async with request.app.db.acquire() as connection:
        result = await connection.execute(products.insert().values(**info))
        product = await result.first()

    return web.json_response({'success': True, 'data': {'id': product.id}})
