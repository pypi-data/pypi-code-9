from __future__ import with_statement
import requests

class TextSharer(object):
    def __init__(self, name):
        self.uploadSuccess = False
        self.objectname    = name

    def readfile(self, path):
        with open(path) as f:
            s = f.read()
        return s

    def uploadfile(self, path):
        text_to_upload = self.readfile(path)
        return self.uploadtext(text_to_upload)

    def uploadtext(self, text):
        return "Must be implemented by the subclass"

    def __str__(self):
        return "I\'m a %s" % self.objectname


