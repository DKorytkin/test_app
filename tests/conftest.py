import os

import pytest
from aiopg.sa import create_engine

from test_app.run import init
from tests.factory import AccountAdmin, AccountManager, AccountUser


@pytest.fixture(scope='session')
def init_db_queries():
    with open('/app/test_app/db_patch/init.sql') as file:
        return file.read()


@pytest.fixture(scope='session')
def cleanup_db_queries():
    with open('/app/test_app/db_patch/cleanup.sql') as file:
        return file.read()


@pytest.fixture()
async def db_engine():
    db = await create_engine(
        user=os.getenv('POSTGRES_USER'),
        database=os.getenv('POSTGRES_DB'),
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT'),
        password=os.getenv('POSTGRES_PASSWORD'),
    )
    yield db
    db.close()
    await db.wait_closed()


@pytest.fixture(autouse=True)
async def cleanup_db(db_engine, cleanup_db_queries, init_db_queries):
    async with db_engine.acquire() as connection:
        await connection.execute(cleanup_db_queries)
        await connection.execute(init_db_queries)
        await connection.execute(AccountAdmin.build())
        await connection.execute(AccountManager.build())
        await connection.execute(AccountUser.build())


@pytest.fixture()
async def build_factory(db_engine):

    async def build(factory):
        async with db_engine.acquire() as connection:
            result = await connection.execute(factory.build())
            data = await result.first()
            return data

    return build


@pytest.fixture()
async def create(db_engine):

    async def build(db_instance):
        async with db_engine.acquire() as connection:
            result = await connection.execute(db_instance)
            data = await result.first()
            return data

    return build


@pytest.fixture()
async def client(aiohttp_client):
    return await aiohttp_client(init)
