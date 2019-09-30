from sources import RSSSource

class Source(RSSSource):
    name = 'Vox'
    url = 'https://www.vox.com'
    feeds = [
        ('https://www.vox.com/rss/business-and-finance/index.xml', 'business'),
        ('https://www.vox.com/rss/policy-and-politics/index.xml', 'politics'),
        ('https://www.vox.com/rss/technology/index.xml', 'technology'),
        ('https://www.vox.com/rss/world/index.xml', 'world'),
        'https://www.vox.com/rss/index.xml',
    ]
    parser_config = {'first-p': True}
