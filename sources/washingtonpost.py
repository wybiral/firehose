from sources import RSSSource

class Source(RSSSource):
    name = 'Washington Post'
    url = 'https://www.washingtonpost.com'
    feeds = [
        'https://www.washingtonpost.com/business/?resType=rss',
        'https://www.washingtonpost.com/national/?resType=rss',
        'https://www.washingtonpost.com/politics/?resType=rss',
        'https://www.washingtonpost.com/business/technology/?resType=rss',
        'https://www.washingtonpost.com/world/?resType=rss',
        'https://www.washingtonpost.com/?resType=rss',
    ]
    parser_config = {'first-p': True}
