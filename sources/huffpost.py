from sources import RSSSource

class Source(RSSSource):
    name = 'HuffPost'
    url = 'https://www.huffpost.com'
    feeds = [
        'https://www.huffpost.com/section/business/feed',
        'https://www.huffpost.com/section/politics/feed',
        'https://www.huffpost.com/section/science/feed',
        'https://www.huffpost.com/section/technology/feed',
        'https://www.huffpost.com/section/us-news/feed',
        'https://www.huffpost.com/section/world-news/feed',
        'https://www.huffpost.com/section/front-page/feed',
    ]
