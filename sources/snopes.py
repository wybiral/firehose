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
                div = soup.find('div', {'class': 'list-group list-group-flush'})
                articles = div.find_all('article')
                for article in reversed(articles):
                    await self._update_article(db, queue, article)

    async def _update_article(self, db, queue, article):
        x = {}
        a = article.find('a')
        x['url'] = a['href']
        div = article.find('div', {'class': 'media-body'})
        x['title'] = div.find('span', {'class': 'title h5'}).get_text()
        # they got rid of pub date, using today
        # (may consider using date from thumbnail URL)
        date = datetime.now()
        x['published'] = date.strftime('%Y-%m-%d')
        x['body'] = div.find('span', {'class': 'subtitle d-flex'}).get_text()
        figure = article.find('figure')
        if figure is not None:
            img = figure.find('img')
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
