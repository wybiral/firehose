from sources import RSSSource

class Source(RSSSource):
    name = 'Slate'
    url = 'https://slate.com'
    feeds = [
        ('https://slate.com/feeds/business.rss', 'business'),
        ('https://slate.com/feeds/news-and-politics.rss', 'politics'),
        ('https://slate.com/feeds/technology.rss', 'technology'),
        'https://slate.com/feeds/all.rss',
    ]
