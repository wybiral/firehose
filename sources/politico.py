from sources import RSSSource

class Source(RSSSource):
    name = 'Politico'
    url = 'https://www.politico.com'
    feeds = [
        ('http://www.politico.com/rss/congress.xml', 'congress'),
        ('https://www.politico.com/rss/defense.xml', 'defense'),
        ('https://www.politico.com/rss/economy.xml', 'economy'),
        'https://www.politico.com/rss/politics08.xml',
    ]
