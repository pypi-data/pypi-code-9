# coding=utf8

import json


class JsonParser(object):
    def __init__(self, to_obj=False, *args, **kwargs):
        self.to_obj = to_obj

    def load(self, *args, **kwargs):
        return json.load(*args, **kwargs)

    def loads(self, *args, **kwargs):
        return json.loads(*args, **kwargs)

    def dump(self, *args, **kwargs):
        return json.dump(*args, **kwargs)

    def dumps(self, *args, **kwargs):
        return json.dumps(*args, **kwargs)


jsonparser = JsonParser()
