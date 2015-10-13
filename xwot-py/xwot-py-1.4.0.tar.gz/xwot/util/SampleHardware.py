import json

class SampleHardware:
    def to_json(self):
        return json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])