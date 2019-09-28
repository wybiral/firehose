from sources import RSSSource

class Source(RSSSource):
    name = 'CBS News'
    url = 'https://www.cbsnews.com'
    feeds = [
        'https://www.cbsnews.com/latest/rss/politics',
        'https://www.cbsnews.com/latest/rss/tech',
        'https://www.cbsnews.com/latest/rss/us',
        'https://www.cbsnews.com/latest/rss/world',
        'https://www.cbsnews.com/latest/rss/main',
    ]
