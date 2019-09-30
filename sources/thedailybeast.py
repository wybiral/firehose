from sources import RSSSource

class Source(RSSSource):
    name = 'The Daily Beast'
    url = 'https://www.thedailybeast.com/'
    feeds = [
        'https://feeds.thedailybeast.com/rss/politics',
        'https://feeds.thedailybeast.com/rss/us-news',
        'https://feeds.thedailybeast.com/rss/world',
        'https://feeds.thedailybeast.com/rss/articles',
    ]
    parser_config = {'first-p': True}
