from sources import RSSSource

class Source(RSSSource):
    name = 'Politico'
    url = 'https://www.politico.com'
    feeds = [
        'http://www.politico.com/rss/congress.xml',
        'https://www.politico.com/rss/defense.xml',
        'https://www.politico.com/rss/economy.xml',
        'https://www.politico.com/rss/politics08.xml',
    ]
