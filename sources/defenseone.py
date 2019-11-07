from sources import RSSSource

class Source(RSSSource):
    name = 'Defense One'
    url = 'https://www.defenseone.com'
    feeds = [
        ('https://www.defenseone.com/rss/politics/', 'politics'),
        ('https://www.defenseone.com/rss/technology/', 'technology'),
        'https://www.defenseone.com/rss/all/',
    ]
