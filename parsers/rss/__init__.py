from bs4 import BeautifulSoup
import datetime
import feedparser
import time

class RSSParser:

    def parse(self, x):
        ''' Parse feed items from x text, return item generator. '''
        # feedparser will perform a request from these strings
        if x[:3] in ('htt', 'ftp', 'fil', 'fee'):
            return None
        feed = feedparser.parse(x)
        entries = feed['entries']
        for entry in reversed(entries):
            url = entry['link']
            update = {}
            if 'id' in entry:
                update['id'] = entry['id']
            else:
                update['id'] = url
            update['url'] = url
            update['title'] = clean_html(entry['title'])
            body = extract_body(entry)
            body = BeautifulSoup(body, 'html.parser')
            update['body'] = self.format_body(body)
            thumb = extract_thumb(entry)
            if thumb:
                update['thumb'] = thumb
            if 'published_parsed' in entry:
                date = entry['published_parsed']
                date = time.strftime('%Y-%m-%d %H:%M:%S', date)
            else:
                date = datetime.datetime.now()
                date = date.strftime('%Y-%m-%d %H:%M:%S')
            update['published'] = date
            yield update

    def format_body(self, body):
        return body.get_text().strip()


def clean_html(raw):
    ''' Clean up HTML from raw text, extracting only the text. '''
    return BeautifulSoup(raw, 'html.parser').get_text().strip()

def extract_body(entry):
    ''' Extract body from RSS item entry. '''
    texts = []
    if 'summary' in entry:
        texts.append(entry['summary'])
    # some publications put the whole article so we search for the true summary
    # by looking for the shortest text/html content if multiple exist.
    if 'content' in entry:
        for content in entry['content']:
            if content['type'] == 'text/html':
                texts.append(content['value'])
    if len(texts) == 0:
        return ''
    texts.sort(key=lambda x: len(x))
    return texts[0]

def extract_thumb(entry):
    ''' Extract thumbnail URL from RSS item entry.
        Different publishers put the thumbnail in different places in the feed
        so this approach checks a number of possibilities, returning None of no
        thumbnail is found.
    '''
    if 'media_thumbnail' in entry and len(entry['media_thumbnail']) > 0:
        return entry['media_thumbnail'][0]['url']
    if 'media_content' in entry and len(entry['media_content']) > 0:
        if 'url' in entry['media_content'][0]:
            return entry['media_content'][0]['url']
    if 'links' in entry and len(entry['links']) > 0:
        imgs = [x for x in entry['links'] if 'image' in x['type']]
        if len(imgs) > 0:
            return imgs[0]['href']
    if 'summary' not in entry:
        return None
    # no media attachment or thumbnail? look for <img> in body...
    soup = BeautifulSoup(entry['summary'], 'html.parser')
    img = soup.find('img')
    if img is None:
        return None
    # filter out 1x1 tracker images
    if img.get('width', None) == '1':
        return None
    # Routers News has a weird image link that gets mistaken for a thumbnail
    # for now, filtering "yIl2AUoC8zA" is a hacky workaround
    if 'yIl2AUoC8zA' in img['src']:
        return None
    return img['src']
