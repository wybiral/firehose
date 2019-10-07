from sources import RSSSource

class Source(RSSSource):
    name = 'ABC News'
    url = 'https://abcnews.go.com/'
    feeds = [
        ('https://abcnews.go.com/abcnews/politicsheadlines', 'politics'),
        ('https://abcnews.go.com/abcnews/technologyheadlines', 'technology'),
        ('https://abcnews.go.com/abcnews/usheadlines', 'us'),
        ('https://abcnews.go.com/abcnews/internationalheadlines', 'world'),
        'https://abcnews.go.com/abcnews/topstories',
    ]

    def format_body(self, body):
        p = body.find('p')
        if p is not None:
            body = p
        return body.get_text().strip()
