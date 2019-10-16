import aiohttp
from bs4 import BeautifulSoup
from sources import BaseSource

class Source(BaseSource):

    name = 'NPR News'
    url = 'https://www.npr.org/sections/news/'

    def __init__(self, module):
        self.module = module
        self.feeds = [
            ('https://www.npr.org/feeds/1006/feed.json', 'business'),
            ('https://www.npr.org/feeds/1014/feed.json', 'politics'),
            ('https://www.npr.org/feeds/1007/feed.json', 'science'),
            ('https://www.npr.org/feeds/1019/feed.json', 'technology'),
            ('https://www.npr.org/feeds/1004/feed.json', 'world'),
            'https://www.npr.org/feeds/1001/feed.json',
        ]

    async def update(self, db, queue):
        headers = {'User-Agent': 'Firehose'}
        async with aiohttp.ClientSession(headers=headers) as s:
            for x in self.feeds:
                if isinstance(x, tuple):
                    url, category = x
                else:
                    url, category = x, None
                async with s.get(url) as r:
                    json = await r.json()
                    for item in json['items']:
                        await self._update_item(db, queue, item, category)

    async def _update_item(self, db, queue, item, category):
        url = item['url']
        url, _ = url.split('?', 1)
        x = {}
        x['url'] = url
        date = item['date_published']
        date = date[:19].replace('T', ' ')
        x['published'] = date
        x['title'] = item['title']
        if 'summary' in item:
            x['body'] = item['summary']
        if 'image' in item:
            x['thumb'] = item['image']
        x['source_name'] = self.name
        x['source_url'] = self.url
        if category is not None:
            x['category'] = category
        x['id'] = self.module + ':' + x['url']
        inserted = await db.insert(x)
        if inserted:
            await queue.put(x)
