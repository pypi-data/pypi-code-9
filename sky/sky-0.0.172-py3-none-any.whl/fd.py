from sky.configs import DEFAULT_CRAWL_CONFIG
from sky.scraper import Scraper

import os
import json

import glob
from lxml import html
from bs4 import UnicodeDammit

# Crawling
config = DEFAULT_CRAWL_CONFIG
config['collections_path'] = '/Users/pascal/'
config['collection_name'] = 'fd'

path = os.path.join(config['collections_path'], config['collection_name'], '*.html')
for filename in glob.glob(path):
    with open(filename, 'rb') as f:
        content = f.read()
        doc = UnicodeDammit(content, is_html=True)

    parser = html.HTMLParser(encoding=doc.original_encoding)
    root = html.document_fromstring(content, parser=parser)
    url = root.xpath('//meta[@property="og:url"]/@content')[0]
    with open(filename.replace('.html', '.json'), 'w') as f:
        json.dump({'url': url, 'html': str(content), 'headers': {}}, f)

skindex = Scraper(config)

skindex.load_local_pages()
skindex.add_template_elements()

res = skindex.process_all()
