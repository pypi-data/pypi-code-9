# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import smart_unicode
from hipster_api.fields import Field


def parse_doc_block(docs):
    docs = smart_unicode(docs)
    blocks = {
        'text': None
    }

    if not docs:
        return blocks

    text = False
    for doc in docs.split('\n'):
        if not doc.strip():
            continue
        doc = doc.strip()

        if doc[0] != ':' and not text:
            blocks['text'] = u"%s\n%s".strip() % (blocks['text'], doc) if blocks['text'] else doc
        else:
            text = True
            val = doc[1:-1].split(' ')
            if len(val) == 1:
                key = val[0]
                val = val[0]
            else:
                key = val.pop(0)
                val = " ".join(val)
            blocks[key] = val

    return blocks


def parse_filed_urls(key, obj):
    if issubclass(obj.__class__, Field):
        struct = {
            'name': key,
            'default': obj.default if obj.default is not None else 'null',
            'methods': obj.methods,
            'type': type(obj.default).__name__,
            'verbose_name': obj.verbose_name
        }
        return struct
    return None


def format_method_urls(item):
    url, cls = item

    text = parse_doc_block(cls.__doc__)['text']
    if text == 'None':
        return None
    item = {'url': url, 'text': text, 'class': cls.__name__}
    methods = {}
    fields = []
    for el in cls.__dict__.itervalues():
        try:

            if el.__name__.lower() in ['get', 'put', 'post', 'delete']:
                methods[el.__name__.lower()] = parse_doc_block(el.__doc__)
            elif el.__name__ == 'Fields':
                fields = list(filter(
                    lambda x: x is not None, [parse_filed_urls(x, y) for x, y in el.__dict__.iteritems()]))

        except AttributeError:
            pass

    def methods_merge_fields_urls(method):
        methods[method]['fields'] = list(filter(lambda x: method in x['methods'], fields))

    list(map(methods_merge_fields_urls, methods.keys()))
    item['methods'] = methods

    return item
