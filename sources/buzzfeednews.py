from sources import RSSSource

class Source(RSSSource):
    name = 'BuzzFeed News'
    url = 'https://www.buzzfeednews.com'
    feeds = [
        ('https://www.buzzfeednews.com/section/politics.xml', 'politics'),
        ('https://www.buzzfeednews.com/section/tech.xml', 'technology'),
        ('https://www.buzzfeednews.com/section/world.xml', 'world'),
        'https://www.buzzfeednews.com/news.xml',
    ]
