from sources import RSSSource

class Source(RSSSource):
    name = 'The Intercept'
    url = 'https://theintercept.com/'
    feeds = [
        'https://theintercept.com/feed/?lang=en',
    ]
