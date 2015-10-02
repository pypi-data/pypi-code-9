# encoding: utf-8

class PockerException(Exception):pass
class PUnsupportedOption(PockerException):pass

class PNotYetImplemented(PockerException):
    def __str__(self):
        return "This functionality isn't implemented yet."

class PExitNonZero(PockerException):
    def __init__(self, resp):
        self.resp = resp

    def __str__(self):
        return self.resp.stderr_raw

    def __unicode__(self):
        return unicode(str(self))



