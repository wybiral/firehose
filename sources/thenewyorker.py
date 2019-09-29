from sources import RSSSource

class Source(RSSSource):
    name = 'The New Yorker'
    url = 'https://www.newyorker.com'
    feeds = [
        'http://www.newyorker.com/feed/tech',
        'http://www.newyorker.com/feed/news',
    ]
