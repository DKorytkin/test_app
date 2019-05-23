from datetime import datetime

import trafaret as t

from tests.factory import AccountUser, Product


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


async def test_empty_orders_for_new_user(client, build_factory):
    user = await build_factory(AccountUser)
    response = await client.get(f'/users/{user.id}/orders')
    assert response.status == 200
    body = await response.json()
    assert body['success'] is True
    assert body['data'] == []


async def test_create_order(client, build_factory):
    user = await build_factory(AccountUser)
    product = await build_factory(Product)
    data = {'user_id': user.id, 'product_ids': [product.id]}
    response = await client.post(f'/orders', data=data)
    assert response.status == 200
    body = await response.json()
    assert body['success'] is True
    assert body['data'] == {'id': 1}


async def test_all_user_orders(client, build_factory):
    user = await build_factory(AccountUser)
    product1 = await build_factory(Product)
    product2 = await build_factory(Product)
    data = {'user_id': user.id, 'product_ids': [product1.id, product2.id]}
    await client.post(f'/orders', data=data)
    await client.post(f'/orders', data=data)
    response = await client.get(f'/users/{user.id}/orders')
    assert response.status == 200
    body = await response.json()
    assert body['success'] is True
    assert body['data'] == [{'id': 1}, {'id': 2}]


async def test_user_order(client, build_factory):
    user = await build_factory(AccountUser)
    product = await build_factory(Product)
    data = {'user_id': user.id, 'product_ids': [product.id]}
    order_response = await client.post(f'/orders', data=data)
    order_json = await order_response.json()
    order_id = order_json['data']['id']
    response = await client.get(f'/users/{user.id}/orders/{order_id}')
    assert response.status == 200
    body = await response.json()
    assert body['success'] is True
    ORDER_SCHEMA.check(body['data'])
