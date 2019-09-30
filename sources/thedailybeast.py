from sources import RSSSource

class Source(RSSSource):
    name = 'The Daily Beast'
    url = 'https://www.thedailybeast.com/'
    feeds = [
        ('https://feeds.thedailybeast.com/rss/politics', 'politics'),
        ('https://feeds.thedailybeast.com/rss/us-news', 'us'),
        ('https://feeds.thedailybeast.com/rss/world', 'world'),
        'https://feeds.thedailybeast.com/rss/articles',
    ]
    parser_config = {'first-p': True}
