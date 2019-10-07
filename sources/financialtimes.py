from sources import RSSSource

class Source(RSSSource):
    name = 'Financial Times'
    url = 'https://www.ft.com'
    feeds = [
        ('https://www.ft.com/technology?format=rss', 'technology'),
        ('https://www.ft.com/world/us?format=rss', 'us'),
        ('https://www.ft.com/world?format=rss', 'world'),
        'https://www.ft.com/?format=rss',
    ]
