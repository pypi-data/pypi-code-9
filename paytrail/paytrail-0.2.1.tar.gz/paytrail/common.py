import hmac

from datetime import datetime
from base64 import b64encode
from hashlib import md5, sha256

def makeTimestamp():
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+0000")

def makeAuthorization(apiName, contentMD5, timestamp, apikey, secret, method, uri):
    '''
    Make the authorization triple. The secret argument must be a bytestring or bytearray.
    '''
    sigData = "%s\n%s\n%s %s\n%s\n%s" % (method, uri, apiName, apikey, timestamp, contentMD5)
    hashedSig = b64encode(hmac.new(secret, sigData.encode('utf8'), sha256).digest()).decode('utf8')

    return "%s %s:%s" % (apiName, apikey, hashedSig)

def makeContentMD5(body):
    return b64encode(md5(body.encode('utf8')).digest()).decode('utf8')

def makeHeaders(apiName, timestamp, apikey, secret, method, uri, body):
    '''
    Return the headers that go into every Paytrail API call. 
    The secret argument must be a bytestring or bytearray.
    '''
    contentMD5 = makeContentMD5(body)
    return {"Timestamp": timestamp,
            "Content-MD5": contentMD5,
            "Authorization": makeAuthorization(apiName, contentMD5, timestamp, apikey, secret, method, uri)}

