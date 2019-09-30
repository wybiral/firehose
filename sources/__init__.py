import aiohttp
import asyncio
from cache import Cache
from parsers.rss import RSSParser


class BaseSource:

    interval = 30

    async def run(self, queue):
        interval = self.interval
        while True:
            await self.update(queue)
            await asyncio.sleep(interval)

    async def update(self, queue):
        raise NotImplemented


class RSSSource(BaseSource):

    name = ''
    url = ''
    feeds = []
    parser_config = {}
    cache_size = 500

    def __init__(self, module):
        self.logfile = 'logs/%s.txt' % module
        self.cache = Cache(size=self.cache_size)
        self.parser = RSSParser(config=self.parser_config)
        self.cache.load(self.logfile)

    async def update(self, queue):
        headers = {'User-Agent': 'Firehose'}
        self.updated = False
        async with aiohttp.ClientSession(headers=headers) as s:
            for x in self.feeds:
                if isinstance(x, tuple):
                    url, category = x
                else:
                    url, category = (x, None)
                async with s.get(url) as r:
                    text = await r.text()
                    await self._update_text(queue, text, category)
        if self.updated:
            self.cache.save(self.logfile)

    async def _update_text(self, queue, text, category):
        for x in self.parser.parse(text):
            url = x['url']
            if url in self.cache:
                continue
            self.updated = True
            self.cache.add(url)
            x['source'] = {
                'name': self.name,
                'url': self.url,
            }
            if category is not None:
                x['source']['category'] = category
            await queue.put(x)
