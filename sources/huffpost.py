from sources import RSSSource

class Source(RSSSource):
    name = 'HuffPost'
    url = 'https://www.huffpost.com'
    feeds = [
        ('https://www.huffpost.com/section/business/feed', 'business'),
        ('https://www.huffpost.com/section/politics/feed', 'politics'),
        ('https://www.huffpost.com/section/science/feed', 'science'),
        ('https://www.huffpost.com/section/technology/feed', 'technology'),
        ('https://www.huffpost.com/section/us-news/feed', 'us'),
        ('https://www.huffpost.com/section/world-news/feed', 'world'),
        'https://www.huffpost.com/section/front-page/feed',
    ]
