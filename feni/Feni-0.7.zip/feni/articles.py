import os
import glob
import yaml
import logging
from .  import exceptions

class Article:
    def __init__(self, name, header, content):
        self.name = name
        self.type = header['type']
        self.permalink = header['permalink'] if 'permalink' in header else None
        self.main = header['main'] if 'main' in header else True
        self.data = header['data']
        self.publish = header['publish'] if 'publish' in header else False
        self.content = content

def get_articles_from(folder, encoding = 'utf-8'):
    paths = os.path.join(folder, '*.md')
    for filename in glob.iglob(paths):
        logging.info("Found article: %s",filename)
        yield get_article_from(folder, filename, encoding=encoding)
                
def get_article_from(folder, filename, encoding = 'utf-8'):
    path = os.path.join(folder, filename)
    with open(path, 'r', encoding=encoding) as f:
        segments = split_file(f)
        if (segments[0] != None):
            header = yaml.load(segments[0])
            header['data'] = get_data(header)
            return Article(os.path.basename(path), header, segments[1])
        else:
            raise exceptions.EmptyArticleError(filename)

def get_data(header):
    r = {}
    for key in header:
        if key[0:5] == 'data-':
            r[key[5:]] = header[key]
    return r

def split_file(f):
    segments = []
    current = ''
    for line in f:
        if line.strip() == '---':
            segments.append(current)
            current = ''
        else:
            current += line
    if current != '':
        segments.append(current)
    elif len(segments) == 0:
        raise exceptions.EmptyFileError
    if len(segments) == 1:
        segments.insert(0, None)
    return segments

            

        
