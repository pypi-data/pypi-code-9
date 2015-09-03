"""
Simple-Rss

A simple RSS feed parser

"""
try:
    import os
    from xml.etree import ElementTree
    import request
except  ImportError:
    pass

__NAME__ = "Simple-Rss"
__version__ = "0.2.0"

def parse(url, tag="./channel/item"):
    """
    Parse
    :param url:
    :param tag:
    :return:
    """
    content = url
    if url.startswith("http://") or url.startswith("https://"):
        rss = requests.get(url)
        if rss.status_code != 200:
            raise Exception("Url Error: Url: <%s> - code <%s>" % url, rss.status_code)
        content = rss.content
    elif os.path.isfile(url):
        with open(url, 'r') as f:
            content = f.read()

    if content:
        tree = ElementTree.fromstring(content)
        return (Element(item) for item in tree.findall(tag))
    else:
        raise ValueError("Parse()  takes a url, filename or XML string")


class Element(object):
    def __init__(self, el):
        self.el = el

    def __getattr__(self, item):
        return self.el.find(item)
