from sources import RSSSource

class Source(RSSSource):
    name = 'Pew Research Center'
    url = 'https://www.pewresearch.org'
    feeds = [
        ('https://www.people-press.org/feed/', 'politics'),
    ]
