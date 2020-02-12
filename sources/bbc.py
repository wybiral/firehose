from sources import RSSSource

class Source(RSSSource):
    name = 'BBC News'
    url = 'https://www.bbc.com/news'
    feeds = [
        ('http://feeds.bbci.co.uk/news/science_and_environment/rss.xml', 'science'),
        ('http://feeds.bbci.co.uk/news/technology/rss.xml', 'technology'),
        ('http://feeds.bbci.co.uk/news/world/rss.xml', 'world'),
        'http://feeds.bbci.co.uk/news/rss.xml',
    ]

    def map(self, x):
        if x['url'].startswith('https://www.bbc.co.uk/sport/'):
            return None
        return x
