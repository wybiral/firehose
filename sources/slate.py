from sources import RSSSource

class Source(RSSSource):
    name = 'Slate'
    url = 'https://slate.com'
    feeds = [
        'https://slate.com/feeds/business.rss',
        'https://slate.com/feeds/news-and-politics.rss',
        'https://slate.com/feeds/technology.rss',
        'https://slate.com/feeds/all.rss',
    ]
