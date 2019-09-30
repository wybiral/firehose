from sources import RSSSource

class Source(RSSSource):
    name = 'The Guardian'
    url = 'https://www.theguardian.com'
    feeds = [
        ('https://www.theguardian.com/us/business/rss', 'business'),
        ('https://www.theguardian.com/us-news/us-politics/rss', 'politics'),
        ('https://www.theguardian.com/science/rss', 'science'),
        ('https://www.theguardian.com/us/technology/rss', 'technology'),
        ('https://www.theguardian.com/us-news/rss', 'us'),
        ('https://www.theguardian.com/world/rss', 'world'),
        'https://www.theguardian.com/uk/rss',
    ]
    parser_config = {'first-p': True}
