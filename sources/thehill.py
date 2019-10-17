from sources import RSSSource

class Source(RSSSource):
    name = 'The Hill'
    url = 'https://thehill.com'
    feeds = [
        ('https://thehill.com/taxonomy/term/1132/feed', 'politics'),
        ('https://thehill.com/taxonomy/term/1131/feed', 'politics'),
        ('https://thehill.com/taxonomy/term/1130/feed', 'politics'),
        ('https://thehill.com/rss/syndicator/19109', 'politics'),
    ]
