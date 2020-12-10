import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime
from sources import BaseSource

class Source(BaseSource):

    name = 'House Intelligence Committee'
    url = 'https://intelligence.house.gov'
    interval = 5 * 60

    def __init__(self, module):
        self.module = module

    async def update(self, db, queue):
        headers = {'User-Agent': 'Firehose'}
        async with aiohttp.ClientSession(headers=headers) as s:
            url = 'https://intelligence.house.gov/news/'
            async with s.get(url) as r:
                text = await r.text()
                soup = BeautifulSoup(text, 'html.parser')
                articles = soup.find_all('article', {'class': 'newsblocker'})
                for article in reversed(articles):
                    await self._update_article(db, queue, article)

    async def _update_article(self, db, queue, article):
        h3 = article.find('h2', {'class': 'newsie-titler'})
        a = h3.find('a')
        url = a['href']
        x = {}
        x['url'] = 'https://intelligence.house.gov' + url
        x['title'] = a.get_text()
        date = article.find('time')
        date = date.get_text()
        date = datetime.strptime(date, '%B %d, %Y')
        x['published'] = date.strftime('%Y-%m-%d')
        div = article.find('div', {'class': 'newsie-content'})
        if div:
            p = div.find('p')
            if p:
                a = p.find('a')
                if a:
                    a.extract()
                x['body'] = p.get_text()
        x['category'] = 'politics'
        x['source_name'] = self.name
        x['source_url'] = self.url
        x['id'] = self.module + ':' + x['url']
        inserted = await db.insert(x)
        if inserted:
            await queue.put(x)
