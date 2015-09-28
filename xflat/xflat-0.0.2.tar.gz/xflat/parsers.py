from lxml import etree
import re
import common
import datetime
import collections



def str_header(headers):

    r = ""
    for k in sorted(headers.keys()):
        r += "# %s\t%s\n" % (k,headers[k])
    return r

def html(blob, name):
    parser = etree.HTMLParser()
    # parsed =
    root = etree.fromstring(blob, parser)
    flattend = common.serialize_node(root)

    xcontent = "\n".join(flattend)
    headers = {
            'parser': 'html',
            'name': name,
            'size-orignal': len(blob),
            'size-xflat': len(xcontent),
            'created': datetime.datetime.utcnow().isoformat(),
        }

    res = str_header(headers)
    res +=  xcontent
    return res


def xml(blob, name):
    xmlns = None
    mo = re.search(r'xmlns="(.*)"', blob)
    if mo:
        xmlns = mo.groups()[0]
        blob = re.sub('xmlns=".*"','',blob)
    root = etree.fromstring(blob)
    flattend = common.serialize_node(root)
    xcontent = "\n".join(flattend)

    headers = {
            'parser': 'xml',
            'name': name,
            'size-orignal': len(blob),
            'size-xflat': len(xcontent),
            'created': datetime.datetime.utcnow().isoformat(),
        }

    if xmlns:
        headers['xmlns'] =  xmlns

    res = str_header(headers)
    res +=  xcontent
    return res


def xflat(xblob):
    histoy = []
    comments = []
    for x in xblob.split("\n"):

        if x.lstrip() and x.lstrip()[0] == "#":
            comments.append(x)
            continue
        path, content, tail, attr = x.decode("utf-8").split("\t")
        parts = path.split("/")
        level = len(parts)
        t = {
            'name':parts[-1],
            'content':common.unescape(content),
            'tail':common.unescape(tail),
            'attrs': attr.strip(),
            'level': level,
            'children': [],
        }
        if t['name'][0] == "!":
            continue
        histoy.append(t)
    root = histoy[0]
    for x in histoy[1:]:
        common.attach_node(root, x)
    return common.str_node(root, True)


XLine = collections.namedtuple("XLine", ['path','name','level','content','tail','attrs'])

def read(xblob):
    for x in xblob.split("\n"):
        if x.lstrip() and x.lstrip()[0] == "#":
            continue
        path, content, tail, attr = x.decode("utf-8").split("\t")
        parts = path.split("/")
        level = len(parts)
        yield(XLine(x, parts[-1],level, common.unescape(content), common.unescape(tail),attr.strip()))
