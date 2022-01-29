import aiohttp
from bs4 import BeautifulSoup
from sources import BaseSource

class Source(BaseSource):

    name = 'Associated Press'
    url = 'https://apnews.com/'

    def __init__(self, module):
        self.module = module
        self.feeds = [
            ('https://apnews.com/apf-science', 'science'),
            ('https://apnews.com/apf-technology', 'technology'),
            ('https://apnews.com/apf-usnews', 'us'),
            ('https://apnews.com/apf-intlnews', 'world'),
            'https://apnews.com/apf-topnews',
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
                    text = await r.text()
                    soup = BeautifulSoup(text, 'html.parser')
                    feed = soup.find('article', {'class': 'feed'})
                    if feed is None:
                        continue
                    articles = feed.find_all('div', recursive=False)
                    for article in reversed(articles):
                        await self._update_article(db, queue, category, article)

    async def _update_article(self, db, queue, category, article):
        x = {}
        if category is not None:
            x['category'] = category
        x['source_name'] = self.name
        x['source_url'] = self.url
        headline = article.find('div', class_='CardHeadline')
        if headline is None:
            return
        a = headline.find('a')
        if a is None:
            a = article.find('a')
        h3 = headline.find('h3')
        x['id'] = self.module + ':' + a['href']
        x['url'] = 'https://apnews.com' + a['href']
        x['title'] = h3.get_text()
        p = article.find('p')
        if p is not None:
            x['body'] = p.get_text()
        span = article.find('span', class_='Timestamp')
        x['published'] = span['data-source'].split('T')[0]
        inserted = await db.insert(x)
        if inserted:
            await queue.put(x)

