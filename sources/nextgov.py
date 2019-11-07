from sources import RSSSource

class Source(RSSSource):
    name = 'Nextgov'
    url = 'https://www.nextgov.com/'
    feeds = [
        'https://www.nextgov.com/rss/all/',
    ]
