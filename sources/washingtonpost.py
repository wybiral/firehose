from sources import RSSSource

class Source(RSSSource):
    name = 'Washington Post'
    url = 'https://www.washingtonpost.com'
    feeds = [
        ('https://www.washingtonpost.com/business/?resType=rss', 'business'),
        ('https://www.washingtonpost.com/politics/?resType=rss', 'politics'),
        ('https://www.washingtonpost.com/business/technology/?resType=rss', 'technology'),
        ('https://www.washingtonpost.com/national/?resType=rss', 'us'),
        ('https://www.washingtonpost.com/world/?resType=rss', 'world'),
        'https://www.washingtonpost.com/?resType=rss',
    ]

    def map(self, x):
        if x['url'].startswith('https://www.washingtonpost.com/opinions/'):
            return None
        if x['url'].startswith('https://www.washingtonpost.com/sports/'):
            return None
        return x

    def format_body(self, body):
        p = body.find('p')
        if p is not None:
            body = p
        return body.get_text().strip()
