import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime
from sources import BaseSource

class Source(BaseSource):

    name = 'House Oversight Committee'
    url = 'https://oversight.house.gov'
    interval = 5 * 60

    def __init__(self, module):
        self.module = module

    async def update(self, db, queue):
        headers = {'User-Agent': 'Firehose'}
        async with aiohttp.ClientSession(headers=headers) as s:
            url = 'https://oversight.house.gov/news'
            async with s.get(url) as r:
                text = await r.text()
                soup = BeautifulSoup(text, 'html.parser')
                div = soup.find('div', {'class': 'pane-content'})
                div = div.find('div', {'class': 'view-content'})
                articles = div.find_all('div')
                for article in reversed(articles):
                    await self._update_article(db, queue, article)

    async def _update_article(self, db, queue, article):
        div = article.find('div', {'class': 'views-field views-field-title'})
        if div is None:
            return
        a = div.find('a')
        url = a['href']
        x = {}
        x['url'] = 'https://oversight.house.gov' + url
        x['title'] = a.get_text()
        s = article.find('span', {'class': 'views-field views-field-created'})
        date = s.get_text().strip()
        date = datetime.strptime(date, '%b %d, %Y')
        x['published'] = date.strftime('%Y-%m-%d')
        d = article.find('div', {
            'class': 'views-field views-field-field-congress-issues',
        })
        if d is not None:
            x['body'] = d.get_text().strip()
        else:
            x['body'] = ''
        x['category'] = 'politics'
        x['source_name'] = self.name
        x['source_url'] = self.url
        x['id'] = self.module + ':' + x['url']
        inserted = await db.insert(x)
        if inserted:
            await queue.put(x)
