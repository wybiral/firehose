import aiohttp
from bs4 import BeautifulSoup
from cache import Cache
from datetime import datetime
from sources import BaseSource

class Source(BaseSource):

    name = 'House Intelligence Committee'
    url = 'https://intelligence.house.gov'
    cache_size = 500
    interval = 60

    def __init__(self, module):
        self.logfile = 'logs/%s.txt' % module
        self.cache = Cache(size=self.cache_size)
        self.cache.load(self.logfile)

    async def update(self, queue):
        headers = {'User-Agent': 'Firehose'}
        self.updated = False
        async with aiohttp.ClientSession(headers=headers) as s:
            url = 'https://intelligence.house.gov/news/'
            async with s.get(url) as r:
                text = await r.text()
                soup = BeautifulSoup(text, 'html.parser')
                articles = soup.find_all('article')
                for article in reversed(articles):
                    await self._update_article(queue, article)
        if self.updated:
            self.cache.save(self.logfile)

    async def _update_article(self, queue, article):
        h3 = article.find('h3', {'class': 'newsie-titler'})
        a = h3.find('a')
        url = a['href']
        if url in self.cache:
            return
        x = {}
        x['url'] = 'https://intelligence.house.gov' + url
        x['title'] = a.get_text()
        date = article.find('time')
        date = date.get_text()
        date = datetime.strptime(date, '%B %d, %Y')
        x['date'] = date.strftime('%Y-%m-%d')
        div = article.find('div', {'class': 'newsie-content'})
        p = div.find('p')
        a = p.find('a')
        a.extract()
        x['body'] = p.get_text()
        x['source'] = {
            'name': self.name,
            'url': self.url,
        }
        self.updated = True
        self.cache.add(url)
        await queue.put(x)
