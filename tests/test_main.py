

async def test_main(client):
    response = await client.get('/')
    assert response.status == 200
    body = await response.json()
    assert body.get('success') is True
    assert body.get('db_connected') is True
    assert isinstance(body.get('version'), str)
