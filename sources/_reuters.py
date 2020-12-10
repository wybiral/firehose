# NOTE: Their RSS feeds seem to be offline.
# Might need to switch to their "wire API".
# See: https://github.com/wybiral/firehose/issues/8

from sources import RSSSource

class Source(RSSSource):
    name = 'Reuters'
    url = 'https://www.reuters.com'
    feeds = [
        ('http://feeds.reuters.com/reuters/businessNews',  'business'),
        ('http://feeds.reuters.com/Reuters/PoliticsNews', 'politics'),
        ('http://feeds.reuters.com/reuters/scienceNews', 'science'),
        ('http://feeds.reuters.com/reuters/technologyNews', 'technology'),
        ('http://feeds.reuters.com/Reuters/domesticNews', 'us'),
        ('http://feeds.reuters.com/Reuters/worldNews', 'world'),
        'http://feeds.reuters.com/reuters/topNews',
    ]

    def map(self, x):
        parts = x['url'].split('?', 1)
        url = parts[0]
        _, id = url.rsplit('-', 1)
        x['url'] = url
        x['id'] = id
        return x