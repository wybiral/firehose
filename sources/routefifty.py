from sources import RSSSource

class Source(RSSSource):
    name = 'Route Fifty'
    url = 'https://www.routefifty.com'
    feeds = [
        'https://www.routefifty.com/rss/all/',
    ]
