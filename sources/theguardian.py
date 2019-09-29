from sources import RSSSource

class Source(RSSSource):
    name = 'The Guardian'
    url = 'https://www.theguardian.com'
    feeds = [
        'https://www.theguardian.com/us/business/rss',
        'https://www.theguardian.com/us-news/us-politics/rss',
        'https://www.theguardian.com/science/rss',
        'https://www.theguardian.com/us/technology/rss',
        'https://www.theguardian.com/us-news/rss',
        'https://www.theguardian.com/world/rss',
        'https://www.theguardian.com/uk/rss',
    ]
    parser_config = {'first-p': True}