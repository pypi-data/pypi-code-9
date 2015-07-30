import json


class Template(object):
    def __init__(self, filename):
        self.filename = filename

    def params(self):
        with open(self.filename, 'rb') as f:
            tmpl = json.loads(f.read())

        return set(tmpl['Parameters'].keys())
