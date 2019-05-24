import pytest
import trafaret as t

from test_app.models.db import Role
from tests import db

SCHEMA = t.Dict({
    t.Key('success'): t.Bool(),
    t.Key('data'): t.List(
        t.Dict({
            'id': t.Int(),
            'role': t.Enum(Role.admin.value, Role.manager.value, Role.user.value)
        })
    )
})


async def test_all_user(client):
    response = await client.get('/users')
    assert response.status == 200
    body = await response.json()
    assert body['success'] is True
    SCHEMA.check(body)


@pytest.mark.parametrize('params', (
    {'role': Role.admin.name},
    {'role': Role.manager.name},
    {'role': Role.user.name},))
async def test_filter_all_user(client, params):
    response = await client.get('/users', params=params)
    assert response.status == 200
    body = await response.json()
    assert body['success'] is True
    SCHEMA.check(body)


async def test_get_user(client, create):
    user_admin = await create(db.user_admin())
    response = await client.get(f'/users/{user_admin.id}')
    assert response.status == 200
    body = await response.json()
    assert body['success'] is True
    assert len(body['data']) == 1
    account = body['data'][0]
    assert account['id'] == user_admin.id
    assert isinstance(account['first_name'], str)
    assert isinstance(account['last_name'], str)
    assert isinstance(account['email'], str)
    assert isinstance(account['created'], str)
    assert isinstance(account['edited'], str)
    profile = account.get('profile')
    assert isinstance(profile, dict)
    assert isinstance(profile['settings'], dict)


@pytest.mark.parametrize('role', (Role.admin.name, Role.manager.name, Role.user.name))
async def test_add_user(client, role):
    data = {
        'first_name': 'TestName',
        'last_name': 'TestSurname',
        'email': 'test.mail@gmail.com',
        'role': role,
    }
    response = await client.post('/users', data=data)
    assert response.status == 200
    body = await response.json()
    assert body['success'] is True
    assert isinstance(body['data']['id'], int)
