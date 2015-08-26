
import json
from codecs import open


def write_dict(d, filepath, encoding='utf-8'):
    with open(filepath, 'w', encoding=encoding) as f:
        f.write(json.dumps(d))


def read_dict(filepath, encoding='utf-8'):
    with open(filepath, 'r', encoding=encoding) as f:
        return json.loads(f.read())
