from sources import RSSSource

class Source(RSSSource):
    name = 'BleepingComputer'
    url = 'https://www.bleepingcomputer.com/'
    feeds = [
        'https://www.bleepingcomputer.com/feed/',
    ]
