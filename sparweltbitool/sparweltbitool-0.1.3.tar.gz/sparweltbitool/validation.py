from voluptuous import Invalid
import re

def Url(msg=None):
    def f(v):

        regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if re.match(regex, str(v)):
            return str(v)
        else:
            raise Invalid(msg or "value is not correct Uniform Resource Locator")
    return f

def TrackableCid(msg=None):
    def f(v):
        regex = re.compile(r'^[A-Z]{2}-[A-Z]{2}-[1-9]{1}[0-9]*$', re.IGNORECASE)
        if re.match(regex, str(v)):
            return str(v)
        else:
            raise Invalid(msg or "value is not correct trackable CID")
    return f
