from bs4 import BeautifulSoup
import datetime
import feedparser
import time

class RSSParser:

    def __init__(self, config=None):
        if config is None:
            config = {}
        self.config = config

    def parse(self, x):
        # feedparser will perform a request from these strings
        if x[:3] in ('htt', 'ftp', 'fil', 'fee'):
            return None
        first_p = self.config.get('first-p', False)
        feed = feedparser.parse(x)
        entries = feed['entries']
        for entry in reversed(entries):
            url = entry['link']
            update = {}
            update['url'] = url
            update['title'] = clean_html(entry['title'])
            body = extract_body(entry)
            body = BeautifulSoup(body, 'html.parser')
            if first_p:
                p = body.find('p')
                if p is not None:
                    body = p
            update['body'] = body.get_text().strip()
            thumb = extract_thumb(entry)
            if thumb:
                update['thumb'] = thumb
            if 'published_parsed' in entry:
                date = entry['published_parsed']
                date = time.strftime('%Y-%m-%d %H:%M:%S', date)
            else:
                date = datetime.datetime.now()
                date = date.strftime('%Y-%m-%d %H:%M:%S')
            update['date'] = date
            yield update


def clean_html(raw):
    return BeautifulSoup(raw, 'html.parser').get_text().strip()

def extract_body(entry):
    texts = []
    texts.append(entry['summary'])
    # some publications put the whole article so we search for the true summary
    # by looking for the shortest text/html content if multiple exist.
    if 'content' in entry:
        for content in entry['content']:
            if content['type'] == 'text/html':
                texts.append(content['value'])
    texts.sort(key=lambda x: len(x))
    return texts[0]

def extract_thumb(entry):
    if 'media_thumbnail' in entry and len(entry['media_thumbnail']) > 0:
        return entry['media_thumbnail'][0]['url']
    if 'media_content' in entry and len(entry['media_content']) > 0:
        if 'url' in entry['media_content'][0]:
            return entry['media_content'][0]['url']
    if 'links' in entry and len(entry['links']) > 0:
        imgs = [x for x in entry['links'] if 'image' in x['type']]
        if len(imgs) > 0:
            return imgs[0]['href']
    # no media attachment or thumbnail? look for <img> in body...
    soup = BeautifulSoup(entry['summary'], 'html.parser')
    img = soup.find('img')
    # Routers has a weird image link that gets mistaken for a thumbnail
    # for now, filtering "yIl2AUoC8zA" is a hacky workaround
    if img and 'yIl2AUoC8zA' not in img['src']:
        return img['src']
    return None