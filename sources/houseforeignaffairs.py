import aiohttp
from bs4 import BeautifulSoup
from cache import Cache
from datetime import datetime
from sources import BaseSource

class Source(BaseSource):

    name = 'House Committee on Foreign Affairs'
    url = 'https://foreignaffairs.house.gov'
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
            url = 'https://foreignaffairs.house.gov/news'
            async with s.get(url) as r:
                text = await r.text()
                soup = BeautifulSoup(text, 'html.parser')
                div = soup.find('div', {'class': 'recordsContainer'})
                table = div.find('table', {'class': 'table recordList'})
                tbody = table.find('tbody')
                articles = tbody.find_all('tr')
                for article in reversed(articles):
                    await self._update_article(queue, article)
        if self.updated:
            self.cache.save(self.logfile)

    async def _update_article(self, queue, article):
        tds = article.find_all('td')
        a = tds[1].find('a')
        url = a['href']
        if url in self.cache:
            return
        x = {}
        x['url'] = 'https://foreignaffairs.house.gov' + url
        x['title'] = a.get_text()
        date = tds[0].get_text()
        date = datetime.strptime(date, '%m/%d/%y')
        x['date'] = date.strftime('%Y-%m-%d')
        x['body'] = ''
        x['source'] = {
            'name': self.name,
            'url': self.url,
        }
        self.updated = True
        self.cache.add(url)
        await queue.put(x)
