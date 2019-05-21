
import trafaret as t
from aiohttp import web
from sqlalchemy import select

from test_app.models.db import accounts
from test_app.handlers.schemas.user import USER_QUERY, USER_ADD


async def users(request):
    user_id = request.match_info.get('user_id')
    try:
        query_params = USER_QUERY.check(request.query)
    except t.dataerror.DataError as e:
        return web.json_response({'success': False, 'error': e.as_dict()})

    db = request.app.db
    query = (
        select([accounts], use_labels=True)
        .order_by(accounts.c.id)
    )
    if user_id:
        query = query.where(accounts.c.id == user_id)

    for filed, value in query_params.items():
        query = query.where(getattr(accounts.c, filed) == value)

    data = []
    async with db.acquire() as connection:
        async for line in connection.execute(query):
            info = {'id': line.accounts_id, 'role': line.accounts_role.value}
            if user_id:
                info.update({
                    'first_name': line.accounts_first_name,
                    'last_name': line.accounts_last_name,
                    'email': line.accounts_email,
                    'profile': {'settings': {}},
                    'created': str(line.accounts_date_created),
                    'edited': str(line.accounts_date_edited),
                })
            data.append(info)
    return web.json_response({'success': True, 'data': data})


async def create_user(request):
    try:
        info = USER_ADD.check(await request.post())
    except t.dataerror.DataError as e:
        return web.json_response({'success': False, 'error': e.as_dict()})

    async with request.app.db.acquire() as connection:
        result = await connection.execute(accounts.insert().values(**info))
        user = await result.first()

    return web.json_response({'success': True, 'data': {'id': user.id}})
