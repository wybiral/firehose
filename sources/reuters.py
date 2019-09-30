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
