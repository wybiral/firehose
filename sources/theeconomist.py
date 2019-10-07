from sources import RSSSource

class Source(RSSSource):
    name = 'The Economist'
    url = 'https://www.economist.com'
    feeds = [
        ('https://www.economist.com/science-and-technology/rss.xml', 'science'),
        ('https://www.economist.com/united-states/rss.xml', 'us'),
        ('https://www.economist.com/international/rss.xml', 'world'),
    ]
