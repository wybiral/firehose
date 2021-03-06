from sources import RSSSource

class Source(RSSSource):
    name = 'The Daily Beast'
    url = 'https://www.thedailybeast.com/'
    feeds = [
        ('https://feeds.thedailybeast.com/rss/politics', 'politics'),
        ('https://feeds.thedailybeast.com/rss/us-news', 'us'),
        ('https://feeds.thedailybeast.com/rss/world', 'world'),
        'https://feeds.thedailybeast.com/rss/articles',
    ]

    def format_body(self, body):
        p = body.find('p')
        if p is not None:
            body = p
        return body.get_text().strip()

    def map(self, x):
        parts = x['url'].split('?', 1)
        url = parts[0]
        x['url'] = url
        x['id'] = url
        return x