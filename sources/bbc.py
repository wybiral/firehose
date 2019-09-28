from sources import RSSSource

class Source(RSSSource):
    name = 'BBC News'
    url = 'https://www.bbc.com/news'
    feeds = [
        'http://feeds.bbci.co.uk/news/science_and_environment/rss.xml',
        'http://feeds.bbci.co.uk/news/technology/rss.xml',
        'http://feeds.bbci.co.uk/news/world/rss.xml',
        'http://feeds.bbci.co.uk/news/rss.xml',
    ]
