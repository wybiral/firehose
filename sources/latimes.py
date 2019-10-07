from sources import RSSSource

class Source(RSSSource):
    name = 'Los Angeles Times'
    url = 'https://www.latimes.com/'
    feeds = [
        ('https://www.latimes.com/politics.rss', 'politics'),
        ('https://www.latimes.com/science.rss', 'science'),
        ('https://www.latimes.com/world-nation', 'world'),
    ]
