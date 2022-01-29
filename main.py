from aiohttp import web
import aiohttp_jinja2
from aiohttp_sse import sse_response
import aiojobs
import asyncio
from database import SQLiteDatabase
import importlib
import jinja2
import json
import os
import datetime

async def pump_firehose(app):
    ''' Spawn all stream source jobs and pump the app['queue'] stream out to
        all Server-Sent Event clients.
    '''
    db = app['db']
    queue = app['queue']
    jobs = await aiojobs.create_scheduler()
    for s in app['sources']:
        await jobs.spawn(s.run(db, queue))
    while True:
        x = await queue.get()
        j = json.dumps(x)
        for client in app['clients']:
            try:
                await client.put(j)
            except:
                pass

async def handle(req):
    print('/')
    return aiohttp_jinja2.render_template('index.html', req, {})

async def streamhandle(req):
    app = req.app
    print('/stream')
    async with sse_response(req) as resp:
        q = asyncio.Queue()
        app['clients'].add(q)
        try:
            while not resp.task.done():
                data = await q.get()
                await resp.send(data)
                q.task_done()
        finally:
            app['clients'].remove(q)
    return resp

async def dailyhandle(req):
    day = req.match_info.get('day', None)
    print('/daily/' + str(day))
    db = req.app['db']
    items = await db.get_day(published=day)
    return aiohttp_jinja2.render_template('daily.html', req, {
        'day': day,
        'items': items,
    })

async def todayhandle(req):
    day = datetime.datetime.now().strftime('%Y-%m-%d')
    return web.HTTPFound(location='/daily/' + day)

async def app_startup(app):
    db = await SQLiteDatabase.connect('firehose.db')
    app['db'] = db
    app['firehose'] = asyncio.create_task(pump_firehose(app))

async def app_cleanup(app):
    await app['db'].close()

def main():
    host = '127.0.0.1'
    port = 8000
    app = web.Application()
    app['queue'] = asyncio.Queue(maxsize=10)
    app['sources'] = []
    app['clients'] = set()
    # setup template env
    loader = jinja2.FileSystemLoader('templates')
    jinja_env = aiohttp_jinja2.setup(app, loader=loader)
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
        web.get('/daily', todayhandle),
        web.get('/daily/{day}', dailyhandle),
        web.get('/stream', streamhandle),
    ])
    app.router.add_static('/static/', path='static', name='static')
    app.on_startup.append(app_startup)
    app.on_cleanup.append(app_cleanup)
    web.run_app(app, host=host, port=port)
    print('\nshutting down...')


if __name__ == '__main__':
    main()
