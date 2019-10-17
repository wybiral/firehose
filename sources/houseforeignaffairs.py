import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime
from sources import BaseSource

class Source(BaseSource):

    name = 'House Committee on Foreign Affairs'
    url = 'https://foreignaffairs.house.gov'
    interval = 5 * 60

    def __init__(self, module):
        self.module = module

    async def update(self, db, queue):
        headers = {'User-Agent': 'Firehose'}
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
                    await self._update_article(db, queue, article)

    async def _update_article(self, db, queue, article):
        tds = article.find_all('td')
        a = tds[1].find('a')
        url = a['href']
        x = {}
        x['url'] = 'https://foreignaffairs.house.gov' + url
        x['title'] = a.get_text()
        date = tds[0].get_text()
        date = datetime.strptime(date, '%m/%d/%y')
        x['published'] = date.strftime('%Y-%m-%d')
        x['body'] = ''
        x['category'] = 'politics'
        x['source_name'] = self.name
        x['source_url'] = self.url
        x['id'] = self.module + ':' + x['url']
        inserted = await db.insert(x)
        if inserted:
            await queue.put(x)
