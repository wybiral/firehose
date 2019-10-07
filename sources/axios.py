from sources import RSSSource

class Source(RSSSource):
    name = 'Axios'
    url = 'https://www.axios.com/'
    feeds = [
        ('https://api.axios.com/feed/politics/', 'politics'),
        ('https://api.axios.com/feed/science/', 'science'),
        ('https://api.axios.com/feed/technology/', 'technology'),
        ('https://api.axios.com/feed/world/', 'world'),
        'https://api.axios.com/feed/',
    ]

    def format_body(self, body):
        p = body.find('p')
        if p is not None:
            body = p
        return body.get_text().strip()
