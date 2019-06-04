from datetime import datetime

import trafaret as t

from tests import db


PRODUCT_SCHEMA = t.List(t.Dict({
    'id': t.Int(),
    'name': t.String(),
    'price': t.Int(),
    'date_created': t.String() >> (lambda d: datetime.strptime(d, '%Y-%m-%d %H:%M:%S.%f')),
    'date_edited': t.String() >> (lambda d: datetime.strptime(d, '%Y-%m-%d %H:%M:%S.%f')),
}))


async def test_empty_products(client):
    response = await client.get('/products')
    assert response.status == 200
    body = await response.json()
    assert body['success'] is True
    assert body['data'] == []


async def test_add_product(client):
    data = {
        'name': 'snickers',
        'price': 150,
    }
    response = await client.post('/products', data=data)
    assert response.status == 200
    body = await response.json()
    assert body['success'] is True
    assert body['data'] == {'id': 1}


async def test_all_products(client, create):
    product = await create(db.product())
    response = await client.get('/products')
    assert response.status == 200
    body = await response.json()
    assert body['success'] is True
    assert body['data'] == [{'id': product.id}]


async def test_get_product(client, create):
    product = await create(db.product())
    response = await client.get(f'/products/{product.id}')
    assert response.status == 200
    body = await response.json()
    assert body['success'] is True
    PRODUCT_SCHEMA.check(body['data'])
