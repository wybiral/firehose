from sources import RSSSource

class Source(RSSSource):
    name = 'VICE'
    url = 'https://www.vice.com'
    feeds = [
        ('https://www.vice.com/en_us/rss/topic/business', 'business'),
        ('https://www.vice.com/en_us/rss/topic/politics', 'politics'),
        ('https://www.vice.com/en_us/rss/topic/science', 'science'),
        ('https://www.vice.com/en_us/rss/topic/technology', 'technology'),
        'https://www.vice.com/en_us/rss',
    ]
