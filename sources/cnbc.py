from sources import RSSSource

class Source(RSSSource):
    name = 'CNBC'
    url = 'https://www.cnbc.com'
    feeds = [
        'https://www.cnbc.com/id/10001147/device/rss/rss.html',
        'https://www.cnbc.com/id/10000113/device/rss/rss.html',
        'https://www.cnbc.com/id/19854910/device/rss/rss.html',
        'https://www.cnbc.com/id/15837362/device/rss/rss.html',
        'https://www.cnbc.com/id/100727362/device/rss/rss.html',
        'https://www.cnbc.com/id/100003114/device/rss/rss.html',
    ]
