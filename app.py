#! /usr/bin/env python3
from aiohttp import web
import weakref

import settings
from game.views import NewGame, GetGame, ListGames, Login, WebSocket
from game.hat import HatGame


async def on_shutdown(app):
    for ws in app.websockets:
        await ws.close(code=1001, message='Server shutdown')


async def shutdown(server, app, handler):
    server.close()
    await server.wait_closed()
    await app.shutdown()
    await handler.finish_connections(10.0)
    await app.cleanup()

app = web.Application()
app.websockets = weakref.WeakSet()
app.games = {}

# default game, temporary, hackish
default_id = '00000000-0000-0000-0000-000000000000'
app.games[default_id] = HatGame(name='Secret Tea')
app.games[default_id].id = default_id

app.add_routes((
    web.get('/', Login, name='login'),
    web.get('/games/{id}', GetGame, name='get_game'),
    web.get('/games', ListGames, name='list_games'),
    web.post('/games', NewGame, name='new_game'),
    web.get('/ws/{id}', WebSocket, name='game'),
    web.get('/ws', WebSocket),  # default game
))

if __name__ == '__main__':
    web.run_app(app, host=settings.SITE_HOST, port=settings.SITE_PORT)
