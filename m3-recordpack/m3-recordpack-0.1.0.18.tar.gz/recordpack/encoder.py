# coding: utf-8
import datetime
import decimal
from json import JSONEncoder


class JsonSerializableEncoder(JSONEncoder):
    def __init__(self, *args, **kwargs):
        kwargs.pop('dict_list', None)
        super(JsonSerializableEncoder, self).__init__(*args, **kwargs)

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            result = '%02d.%02d.%04d %02d:%02d:%02d' % (
                obj.day, obj.month, obj.year, obj.hour, obj.minute, obj.second)
        elif isinstance(obj, datetime.date):
            result = '%02d.%02d.%04d' % (obj.day, obj.month, obj.year)
        elif isinstance(obj, datetime.time):
            result = obj.strftime('%H:%M')
        elif isinstance(obj, decimal.Decimal):
            result = str(obj)
        else:
            result = {}

            for k, v in obj.__dict__.iteritems():
                if not k.startswith('_'):
                    result[k] = v

            cls = obj.__class__

            for attname in dir(cls):
                if not attname.startswith('_'):
                    try:
                        cls_attr = getattr(cls, attname)
                    except Exception:
                        continue
                    if getattr(cls_attr, 'json_encode', False):
                        value = getattr(obj, attname)
                        if callable(value):
                            result[attname] = value()
                        else:
                            result[attname] = value
        return result
