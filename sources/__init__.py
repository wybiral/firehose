import aiohttp
import asyncio
from parsers.rss import RSSParser


class BaseSource:

    interval = 60

    async def run(self, db, queue):
        interval = self.interval
        while True:
            try:
                await self.update(db, queue)
            except aiohttp.ClientConnectorError:
                pass
            await asyncio.sleep(interval)

    async def update(self, db, queue):
        raise NotImplemented


class RSSSource(BaseSource):

    name = ''
    url = ''
    feeds = []

    def __init__(self, module):
        self.module = module
        self.parser = RSSParser()
        if hasattr(self, 'format_body'):
            self.parser.format_body = self.format_body

    def map(self, x):
        return x

    async def update(self, db, queue):
        headers = {'User-Agent': 'Firehose'}
        async with aiohttp.ClientSession(headers=headers) as s:
            for x in self.feeds:
                if isinstance(x, tuple):
                    url, category = x
                else:
                    url, category = (x, None)
                async with s.get(url) as r:
                    text = await r.text()
                    await self._update_text(db, queue, text, category)

    async def _update_text(self, db, queue, text, category):
        for x in self.parser.parse(text):
            if category is not None:
                x['category'] = category
            x['source_name'] = self.name
            x['source_url'] = self.url
            x = self.map(x)
            if x is None:
                continue
            x['id'] = self.module + ':' + x['id']
            inserted = await db.insert(x)
            if inserted:
                await queue.put(x)
