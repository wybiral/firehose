from sources import RSSSource

class Source(RSSSource):
    name = 'Ars Technica'
    url = 'https://arstechnica.com'
    feeds = [
        ('http://feeds.arstechnica.com/arstechnica/business', 'business'),
        ('http://feeds.arstechnica.com/arstechnica/gadgets', 'gadgets'),
        ('http://feeds.arstechnica.com/arstechnica/science', 'science'),
        ('http://feeds.arstechnica.com/arstechnica/security', 'security'),
        ('http://feeds.arstechnica.com/arstechnica/software', 'software'),
        'http://feeds.arstechnica.com/arstechnica/index',
    ]
    parser_config = {'first-p': True}
