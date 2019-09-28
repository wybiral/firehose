from sources import RSSSource

class Source(RSSSource):
    name = 'Ars Technica'
    url = 'https://arstechnica.com'
    feeds = [
        'http://feeds.arstechnica.com/arstechnica/business',
        'http://feeds.arstechnica.com/arstechnica/gadgets',
        'http://feeds.arstechnica.com/arstechnica/science',
        'http://feeds.arstechnica.com/arstechnica/security',
        'http://feeds.arstechnica.com/arstechnica/software',
        'http://feeds.arstechnica.com/arstechnica/index',
    ]
    parser_config = {'first-p': True}
