import aiohttp
from bs4 import BeautifulSoup
from cache import Cache
from sources import BaseSource

class Source(BaseSource):

    name = 'NPR News'
    url = 'https://www.npr.org/sections/news/'
    cache_size = 500

    def __init__(self, module):
        self.logfile = 'logs/%s.txt' % module
        self.cache = Cache(size=self.cache_size)
        self.cache.load(self.logfile)
        self.feeds = [
            'https://www.npr.org/feeds/1006/feed.json',
            'https://www.npr.org/feeds/1014/feed.json',
            'https://www.npr.org/feeds/1007/feed.json',
            'https://www.npr.org/feeds/1019/feed.json',
            'https://www.npr.org/feeds/1004/feed.json',
            'https://www.npr.org/feeds/1001/feed.json',
        ]

    async def update(self, queue):
        headers = {'User-Agent': 'Firehose'}
        self.updated = False
        async with aiohttp.ClientSession(headers=headers) as s:
            for url in self.feeds:
                async with s.get(url) as r:
                    json = await r.json()
                    for item in json['items']:
                        await self._update_item(queue, item)
        if self.updated:
            self.cache.save(self.logfile)

    async def _update_item(self, queue, item):
        url = item['url']
        url, _ = url.split('?', 1)
        if url in self.cache:
            return
        x = {}
        x['url'] = url
        date = item['date_published']
        date = date[:19].replace('T', ' ')
        x['date'] = date
        x['title'] = item['title']
        if 'summary' in item:
            x['body'] = item['summary']
        if 'image' in item:
            x['thumb'] = item['image']
        x['source'] = {
            'name': self.name,
            'url': self.url,
        }
        self.updated = True
        self.cache.add(url)
        await queue.put(x)
