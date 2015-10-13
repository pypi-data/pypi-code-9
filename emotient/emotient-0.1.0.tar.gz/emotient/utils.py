import collections
import six

from dateutil import parser


def get_ids(media):
    def _get_id(obj):
        if isinstance(obj, six.string_types):
            id_str = obj
        elif hasattr(obj, 'id'):
            id_str = obj.id
        else:
            raise AttributeError()

        return id_str

    if not isinstance(media, six.string_types) and isinstance(media, collections.Iterable):
        ids = [_get_id(i) for i in media]
    else:
        ids = [_get_id(media)]

    return ids


def parse_dts(data):
    if not isinstance(data, dict):
        return

    for key in data:
        if isinstance(key, six.string_types) and key.endswith('_at') and isinstance(data[key], six.string_types):
            try:
                dt = parser.parse(data[key])
            except ValueError:
                continue

            data[key] = dt
