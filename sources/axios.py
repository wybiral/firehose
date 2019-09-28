from sources import RSSSource

class Source(RSSSource):
    name = 'Axios'
    url = 'https://www.axios.com/'
    feeds = [
        'https://api.axios.com/feed/politics/',
        'https://api.axios.com/feed/science/',
        'https://api.axios.com/feed/technology/',
        'https://api.axios.com/feed/world/',
        'https://api.axios.com/feed/',
    ]
    parser_config = {'first-p': True}
