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

    def __init__(self):
        self.cache = Cache(size=self.cache_size)
        self.parser = RSSParser(config=self.parser_config)

    async def update(self, queue):
        headers = {'User-Agent': 'Firehose'}
        async with aiohttp.ClientSession(headers=headers) as s:
            for url in self.feeds:
                async with s.get(url) as r:
                    text = await r.text()
                    await self._update_text(queue, text)

    async def _update_text(self, queue, text):
        for x in self.parser.parse(text):
            url = x['url']
            if url in self.cache:
                continue
            self.cache.add(url)
            x['source'] = {
                'name': self.name,
                'url': self.url,
            }
            await queue.put(x)
