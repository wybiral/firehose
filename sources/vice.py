from sources import RSSSource

class Source(RSSSource):
    name = 'VICE'
    url = 'https://www.vice.com'
    feeds = [
        'https://www.vice.com/en_us/rss/topic/business',
        'https://www.vice.com/en_us/rss/topic/politics',
        'https://www.vice.com/en_us/rss/topic/science',
        'https://www.vice.com/en_us/rss/topic/technology',
        'https://www.vice.com/en_us/rss',
    ]
