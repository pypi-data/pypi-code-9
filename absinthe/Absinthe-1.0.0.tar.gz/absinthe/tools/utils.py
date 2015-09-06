
import importlib
import os
import urllib2, urllib
import re
import sys
import json

def ucfirst(str):
    return str[0].upper() + str[1:]

def split_uppercase(str):
    return re.findall('[A-Z][^A-Z]*', str)

def xml_element_to_storage(element):

    res = Storage()
    for item in element:
        res[item.tag] = item.text

    return res

def extend_path(root_dir, paths):
    new_paths = []
    for path in paths:
        pp = [root_dir]
        if type(path) is list:
            pp.extend(path)
        else:
            pp.append(path)

        new_path = os.path.join(*pp)
        new_paths.append(new_path)

    sys.path.extend(new_paths)

class Platforms():
    folders = dict(
        win32 = 'win',
        linux2 = 'linux',
        linux = 'linux',
    )

    def get_folder(self):
        platform = sys.platform
        if platform not in self.folders:
            raise Exception('Unknown platform %s' % platform)

        return self.folders[platform]

    def import_class(self, name):
        folder = self.get_folder()
        file_name = '_'.join(split_uppercase(name)).lower()
        module = importlib.import_module('%s.%s' % (folder, file_name))
        return getattr(module, name)

class Storage(dict):

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value

    def __hasattr__(self, key):
        return key in self


class FileReader(object):
    def read_all(self, file_name):
        with open(file_name) as f:
            content = f.read()
        return content


class SimpleResponse(Storage):
    def __init__(self, code, message = ''):
        self.code = code
        self.message = message

    @staticmethod
    def from_string(response):
        try:
            data = json.loads(response)
            return SimpleResponse(data['code'], data['message'])
        except:
            raise

    def __str__(self):
        return "Code: %r, message: %s" % (self.code, self.message)

class HTTPResponse(object):
    def __init__(self, code, content, headers = {}):
        self.code = code
        self.content = content
        self.headers = headers

    def __str__(self):
        return "code: %d, headers: %s, content: %s" % (self.code, self.headers, self.content)

class URLLoader(object):
    def load(self, url, data = None, headers = {}):

        if data:
            data = urllib.urlencode(data)

        req = urllib2.Request(url, data, headers)

        try:
            response = urllib2.urlopen(req)
            return HTTPResponse(response.getcode(), response.read(), response.info().dict)
        except urllib2.URLError, e:
            return HTTPResponse(e.code, e.read(), e.info().dict)
