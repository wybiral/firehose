from sources import RSSSource

class Source(RSSSource):
    name = 'BuzzFeed News'
    url = 'https://www.buzzfeednews.com'
    feeds = [
        'https://www.buzzfeednews.com/section/politics.xml',
        'https://www.buzzfeednews.com/section/tech.xml',
        'https://www.buzzfeednews.com/section/world.xml',
        'https://www.buzzfeednews.com/news.xml',
    ]
