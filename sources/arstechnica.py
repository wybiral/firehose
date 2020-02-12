from sources import RSSSource

class Source(RSSSource):
    name = 'Ars Technica'
    url = 'https://arstechnica.com'
    feeds = [
        ('http://feeds.arstechnica.com/arstechnica/business', 'business'),
        ('http://feeds.arstechnica.com/arstechnica/gadgets', 'technology'),
        ('http://feeds.arstechnica.com/arstechnica/science', 'science'),
        ('http://feeds.arstechnica.com/arstechnica/security', 'technology'),
        ('http://feeds.arstechnica.com/arstechnica/software', 'technology'),
        'http://feeds.arstechnica.com/arstechnica/index',
    ]

    def map(self, x):
        _, x['id'] = x['url'].rsplit('?p=', 1)
        return x

    def format_body(self, body):
        p = body.find('p')
        if p is not None:
            body = p
        return body.get_text().strip()
