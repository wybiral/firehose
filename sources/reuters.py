from sources import RSSSource

class Source(RSSSource):
    name = 'Reuters'
    url = 'https://www.reuters.com'
    feeds = [
        'http://feeds.reuters.com/reuters/businessNews',
        'http://feeds.reuters.com/news/wealth',
        'http://feeds.reuters.com/Reuters/PoliticsNews',
        'http://feeds.reuters.com/reuters/scienceNews',
        'http://feeds.reuters.com/reuters/technologyNews',
        'http://feeds.reuters.com/Reuters/domesticNews',
        'http://feeds.reuters.com/Reuters/worldNews',
        'http://feeds.reuters.com/reuters/topNews',
    ]
