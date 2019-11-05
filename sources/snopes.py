import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime
from sources import BaseSource

class Source(BaseSource):

    name = 'Snopes'
    url = 'https://www.snopes.com'

    def __init__(self, module):
        self.module = module

    async def update(self, db, queue):
        headers = {'User-Agent': 'Firehose'}
        async with aiohttp.ClientSession(headers=headers) as s:
            url = 'https://www.snopes.com/fact-check/'
            async with s.get(url) as r:
                text = await r.text()
                soup = BeautifulSoup(text, 'html.parser')
                div = soup.find('div', {'class': 'media-list'})
                articles = div.find_all('article', {'class': 'media-wrapper'})
                for article in reversed(articles):
                    await self._update_article(db, queue, article)

    async def _update_article(self, db, queue, article):
        x = {}
        a = article.find('a')
        x['url'] = a['href']
        x['title'] = a.find('h5').get_text()
        li = a.find('li', {'class': 'date breadcrumb-item'})
        date = datetime.strptime(li.get_text().strip(), '%d %B %Y')
        date = date.strftime('%Y-%m-%d')
        x['published'] = date
        p = a.find('p', {'class': 'subtitle'})
        x['body'] = p.get_text()
        img = a.find('img')
        if img is not None:
            srcset = img['data-lazy-srcset']
            srcset = srcset.split('w,')
            x['thumb'] = srcset[1].split(' ')[0]
        x['source_name'] = self.name
        x['source_url'] = self.url
        x['id'] = self.module + ':' + x['url']
        inserted = await db.insert(x)
        if inserted:
            await queue.put(x)
