from sources import RSSSource

class Source(RSSSource):
    name = 'ABC News'
    url = 'https://abcnews.go.com/'
    feeds = [
        'https://abcnews.go.com/abcnews/politicsheadlines',
        'https://abcnews.go.com/abcnews/technologyheadlines',
        'https://abcnews.go.com/abcnews/usheadlines',
        'https://abcnews.go.com/abcnews/internationalheadlines',
        'https://abcnews.go.com/abcnews/topstories',
    ]
    parser_config = {'first-p': True}
