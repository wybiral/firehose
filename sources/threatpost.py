from sources import RSSSource

class Source(RSSSource):
    name = 'Threatpost'
    url = 'https://threatpost.com/'
    feeds = [
        ('https://threatpost.com/feed/', 'technology'),
    ]
