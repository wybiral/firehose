from sources import RSSSource

class Source(RSSSource):
    name = 'ProPublica'
    url = 'https://www.propublica.org/'
    feeds = [
        'http://feeds.propublica.org/propublica/main',
    ]

    def format_body(self, body):
        for p in body.find_all('p', {'class': 'byline'}):
            p.extract()
        for div in body.find_all('div', {'class': 'note'}):
            div.extract()
        p = body.find('p')
        if p is not None:
            body = p
        return body.get_text().strip()
