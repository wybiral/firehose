from aiohttp import web
import aiohttp_jinja2
import aiojobs
import asyncio
import importlib
import jinja2
import json
import os
from sources.axios import Source

async def pump_firehose(app):
    ''' Spawn all stream source jobs and pump the app['queue'] stream out to
        all app['websockets']
    '''
    queue = app['queue']
    jobs = await aiojobs.create_scheduler()
    for s in app['sources']:
        await jobs.spawn(s.run(queue))
    while True:
        if len(app['websockets']) == 0:
            # don't bother if no clients
            await asyncio.sleep(1)
            continue
        x = await queue.get()
        j = json.dumps(x)
        for ws in app['websockets']:
            try:
                await ws.send_str(j)
            except:
                pass
        await asyncio.sleep(0.1)

async def handle(req):
    print('/')
    return aiohttp_jinja2.render_template('index.html', req, {})

async def wshandle(req):
    print('/socket')
    ws = web.WebSocketResponse(heartbeat=5)
    await ws.prepare(req)
    req.app['websockets'].add(ws)
    async for msg in ws:
        if msg.type == web.WSMsgType.close:
            break
    req.app['websockets'].remove(ws)
    return ws

async def start_background_tasks(app):
    app['firehose'] = asyncio.create_task(pump_firehose(app))

def main():
    host = '127.0.0.1'
    port = 8000
    app = web.Application()
    app['queue'] = asyncio.Queue(maxsize=10)
    app['sources'] = []
    app['websockets'] = set()
    # setup template env
    loader = jinja2.FileSystemLoader('templates')
    jinja_env = aiohttp_jinja2.setup(app, loader=loader)
    # create cache log path
    os.makedirs('logs', exist_ok=True)
    # instantiate all Source objects from sources module
    for name in os.listdir('sources'):
        if name.startswith('_'):
            continue
        if name.endswith('.py'):
            name = name[:-3]
        m = importlib.import_module('sources.' + name)
        if hasattr(m, 'Source'):
            app['sources'].append(m.Source(name))
    # web app routes
    app.add_routes([
        web.get('/', handle),
        web.get('/socket', wshandle),
    ])
    app.router.add_static('/static/', path='static', name='static')
    app.on_startup.append(start_background_tasks)
    web.run_app(app, host=host, port=port)
    print('\nshutting down...')


if __name__ == '__main__':
    main()
