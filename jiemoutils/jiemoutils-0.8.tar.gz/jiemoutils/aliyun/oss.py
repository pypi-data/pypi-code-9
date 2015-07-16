import base64
import hmac
from hashlib import sha1
import time
import urllib.request
from jiemoutils import aliyun


HOST="oss.aliyuncs.com"


def _oss_file_url(method, bucket, filename):
    now = int(time.time())
    tnow = now - (now % 1800) + 3800 #避免每个时刻url都不一样
    tosign = "%s\n\n\n%d\n/%s/%s" % (method, tnow, bucket, filename)
    if method == 'PUT' or method == 'POST':
        tnow = int(time.time() + 1000)
        tosign = "%s\n\napplication/octet-stream\n%d\n/%s/%s" % (method, tnow, bucket, filename)
    h = hmac.new(aliyun.getDefaultAppInfo().accessKeySecret.encode(),
             tosign.encode(),
             sha1)
    sign = urllib.request.quote(base64.encodebytes(h.digest()).strip())
    return 'http://%s.oss-cn-hangzhou.aliyuncs.com/%s?OSSAccessKeyId=%s&Expires=%d&Signature=%s' % (
        bucket, filename, aliyun.getDefaultAppInfo().accessKeyId, tnow, sign
    )

def get_file_url(bucket, filename):
    return _oss_file_url('GET', bucket, filename)


def http_put(bucket, filename, cont):
    url = _oss_file_url('PUT', bucket, filename)
    req = urllib.request.Request(url, cont)
    req.get_method = lambda: 'PUT'
    req.add_header('content-type', 'application/octet-stream')
    try:
        return urllib.request.urlopen(req)
    except urllib.request.HTTPError as e:
        print(e)

