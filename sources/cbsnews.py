from sources import RSSSource

class Source(RSSSource):
    name = 'CBS News'
    url = 'https://www.cbsnews.com'
    feeds = [
        ('https://www.cbsnews.com/latest/rss/politics', 'politics'),
        ('https://www.cbsnews.com/latest/rss/tech', 'technology'),
        ('https://www.cbsnews.com/latest/rss/us', 'us'),
        ('https://www.cbsnews.com/latest/rss/world', 'world'),
        'https://www.cbsnews.com/latest/rss/main',
    ]

    def map(self, x):
        if x['url'].startswith('https://www.cbsnews.com/video/'):
            return None
        return x
