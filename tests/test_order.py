from datetime import datetime

import trafaret as t

from tests import db


ORDER_SCHEMA = t.Dict({
    'id': t.Int(),
    'account_id': t.Int(),
    'date_created': t.String() >> (lambda d: datetime.strptime(d, '%Y-%m-%d %H:%M:%S.%f')),
    'date_edited': t.String() >> (lambda d: datetime.strptime(d, '%Y-%m-%d %H:%M:%S.%f')),
    'products': t.List(t.Dict({
        'id': t.Int(),
        'name': t.String(),
        'price': t.Int(),
    })),
})


async def test_empty_orders_for_new_user(client, create):
    user = await create(db.user())
    response = await client.get(f'/users/{user.id}/orders')
    assert response.status == 200
    body = await response.json()
    assert body['success'] is True
    assert body['data'] == []


async def test_create_order(client, create):
    user = await create(db.user())
    product = await create(db.product())
    data = {'user_id': user.id, 'product_ids': [product.id]}
    response = await client.post(f'/orders', data=data)
    assert response.status == 200
    body = await response.json()
    assert body['success'] is True
    assert body['data'] == {'id': 1}


async def test_all_user_orders(client, create):
    user = await create(db.user())
    product1 = await create(db.product())
    product2 = await create(db.product())
    data = {'user_id': user.id, 'product_ids': [product1.id, product2.id]}
    await client.post(f'/orders', data=data)
    response = await client.get(f'/users/{user.id}/orders')
    assert response.status == 200
    body = await response.json()
    assert body['success'] is True
    assert body['data'] == [{'id': 1}]


async def test_user_order(client, create):
    user = await create(db.user())
    product = await create(db.product())
    data = {'user_id': user.id, 'product_ids': [product.id]}
    order_response = await client.post(f'/orders', data=data)
    order_json = await order_response.json()
    order_id = order_json['data']['id']
    response = await client.get(f'/users/{user.id}/orders/{order_id}')
    assert response.status == 200
    body = await response.json()
    assert body['success'] is True
    ORDER_SCHEMA.check(body['data'])
