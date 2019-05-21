
from aiohttp import web


async def main(request):
    return web.json_response({'success': True, 'version': 'v1.23.4', 'db_connected': True})
