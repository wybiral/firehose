import aiohttp
from bs4 import BeautifulSoup
from sources import BaseSource

class Source(BaseSource):

    name = 'C-SPAN'
    url = 'https://www.c-span.org'

    def __init__(self, module):
        self.module = module

    async def update(self, db, queue):
        headers = {'User-Agent': 'Firehose'}
        async with aiohttp.ClientSession(headers=headers) as s:
            url = 'https://www.c-span.org/search/'
            query = 'searchtype=Videos&sort=Most+Recent+Airing&ajax&page=1'
            async with s.get(url + '?' + query) as r:
                text = await r.text()
                soup = BeautifulSoup(text, 'html.parser')
                videos = soup.find_all('li', {'class': 'onevid'})
                for video in reversed(videos):
                    await self._update_video(db, queue, video)

    async def _update_video(self, db, queue, video):
        text = video.find('div', {'class': 'text'})
        url = text.find('a', {'class': 'title'})['href']
        x = {}
        text = video.find('div', {'class': 'text'})
        title_a = text.find('a', {'class': 'title'})
        url = title_a['href']
        x['url'] = url
        x['title'] = title_a.find('h3').get_text()
        dates = text.find_all('time')
        date = ''
        if len(dates) > 0 and 'datetime' not in dates[-1]:
            date = dates[-1]['datetime']
        x['published'] = date
        body_p = text.find('p', {'class': 'abstract'})
        if body_p:
            x['body'] = body_p.get_text()
        thumb_a = video.find('a', {'class': 'thumb'})
        x['thumb'] = thumb_a.find_all('img')[0]['src']
        x['category'] = 'politics'
        x['source_name'] = self.name
        x['source_url'] = self.url
        x['id'] = self.module + ':' + x['url']
        inserted = await db.insert(x)
        if inserted:
            await queue.put(x)
