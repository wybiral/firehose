import aiohttp
from bs4 import BeautifulSoup
from cache import Cache
from datetime import datetime
from sources import BaseSource

class Source(BaseSource):

    name = 'House Oversight Committee'
    url = 'https://oversight.house.gov'
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
            url = 'https://oversight.house.gov/news'
            async with s.get(url) as r:
                text = await r.text()
                soup = BeautifulSoup(text, 'html.parser')
                div = soup.find('div', {'class': 'pane-content'})
                div = div.find('div', {'class': 'view-content'})
                articles = div.find_all('div')
                for article in reversed(articles):
                    await self._update_article(queue, article)
        if self.updated:
            self.cache.save(self.logfile)

    async def _update_article(self, queue, article):
        div = article.find('div', {'class': 'views-field views-field-title'})
        if div is None:
            return
        a = div.find('a')
        url = a['href']
        if url in self.cache:
            return
        x = {}
        x['url'] = 'https://oversight.house.gov' + url
        x['title'] = a.get_text()
        s = article.find('span', {'class': 'views-field views-field-created'})
        date = s.get_text().strip()
        date = datetime.strptime(date, '%b %d, %Y')
        x['date'] = date.strftime('%Y-%m-%d')
        d = article.find('div', {
            'class': 'views-field views-field-field-congress-issues',
        })
        if d is not None:
            x['body'] = d.get_text().strip()
        else:
            x['body'] = ''
        x['source'] = {
            'name': self.name,
            'url': self.url,
        }
        self.updated = True
        self.cache.add(url)
        await queue.put(x)
