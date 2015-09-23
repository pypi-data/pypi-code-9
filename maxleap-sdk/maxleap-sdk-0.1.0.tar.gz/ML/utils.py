# coding: utf-8

import copy
import json
import gzip
from cStringIO import StringIO
from datetime import datetime

import arrow
import iso8601
from dateutil import tz

import ML
from ML import operation

__author__ = 'czhou <czhou@ilegendsoft.com>'


def get_dumpable_types():
    return (
        ML.ACL,
        ML.GeoPoint,
        ML.Relation,
        operation.BaseOp,
    )


def encode(value, disallow_objects=False):
    if isinstance(value, datetime):
        tzinfo = value.tzinfo
        if tzinfo is None:
            tzinfo = tz.tzlocal()
        return {
            '__type': 'Date',
            'iso': arrow.get(value, tzinfo).to('utc').format('YYYY-MM-DDTHH:mm:ss.SSS') + 'Z',
        }

    if isinstance(value, ML.Object):
        if disallow_objects:
            raise ValueError('ML.Object not allowed')
        return value._to_pointer()

    if isinstance(value, ML.File):
        if not value.url and not value.id:
            raise ValueError('Tried to save an object containing an unsaved file.')
        return {
            '__type': 'File',
            'id': value.id,
            'name': value.name,
            'url': value.url,
        }


    if isinstance(value, get_dumpable_types()):
        return value.dump()

    if isinstance(value, (tuple, list)):
        return [encode(x, disallow_objects) for x in value]

    if isinstance(value, dict):
        return  dict([(k, encode(v, disallow_objects)) for k, v in value.iteritems()])

    return value





def decode(key, value):
    if isinstance(value, get_dumpable_types()):
        return value

    if isinstance(value, (tuple, list)):
        return [decode(key, x) for x in value]

    if not isinstance(value, dict):
        return value

    if '__type' not in value:
        return dict([(k, decode(k, v)) for k, v in value.iteritems()])

    _type = value['__type']

    if _type == 'Pointer':
        value = copy.deepcopy(value)
        class_name = value['className']
        pointer = ML.Object.create(class_name)
        if 'createdAt' in value:
            value.pop('__type')
            value.pop('className')
            pointer._finish_fetch(value, True)
        else:
            pointer._finish_fetch({'objectId': value['objectId']}, False)
        return pointer

    if _type == 'Object':
        value = copy.deepcopy(value)
        class_name = value['className']
        value.pop('__type')
        value.pop('class_name')
        obj = ML.Object.create(class_name)
        obj._finish_fetch(value, True)
        return obj

    if _type == 'Date':
        return arrow.get(iso8601.parse_date(value['iso'])).to('local').datetime

    if _type == 'GeoPoint':
        return ML.GeoPoint(latitude=value['latitude'], longitude=value['longitude'])

    if key == 'ACL':
        if isinstance(value, ML.ACL):
            return value
        return ML.ACL(value)

    if _type == 'Relation':
        relation = ML.Relation(None, key)
        relation.target_class_name = value['className']
        return relation

    if _type == 'File':
        f = ML.File(value['name'])
        meta_data = value.get('metaData')
        if meta_data:
            f._metadata = meta_data
        f._url = value['url']
        f.id = ''
        return f


def traverse_object(obj, callback, seen=None):
    seen = seen or set()

    if isinstance(obj, ML.Object):
        if obj in seen:
            return
        seen.add(obj)
        traverse_object(obj.attributes, callback, seen)
        return callback(obj)

    if isinstance(obj, (ML.Relation, ML.File)):
        return callback(obj)

    if isinstance(obj, (list, tuple)):
        for idx, child in enumerate(obj):
            new_child = traverse_object(child, callback, seen)
            if new_child:
                obj[idx] = new_child
        return callback(obj)

    if isinstance(obj, dict):
        for key, child in obj.iteritems():
            new_child = traverse_object(child, callback, seen)
            if new_child:
                obj[key] = new_child
        return callback(obj)

    return callback(obj)

def response_to_json(response):
    """
    hack for requests in python 2.6
    """
    if isinstance(response, ML.Response):
        return json.loads(response.data)

    content = response.content
    # hack for requests in python 2.6
    if 'application/json' in response.headers.get('Content-Type',''):
        if content[:2] == '\x1f\x8b':
            f = StringIO(content)
            g = gzip.GzipFile(fileobj=f)
            content = g.read()
            g.close()
            f.close()
    return json.loads(content)
