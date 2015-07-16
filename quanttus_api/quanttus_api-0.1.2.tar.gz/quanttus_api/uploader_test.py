import uploader
import multiprocessing
#import requests
import sys

from functools import wraps
from flask import Flask, request, Response
app = Flask(__name__)

__author__ = 'jpercent'


def check_auth(username, password):
    return username == 'admin' and password == 'secret'


def authenticate():
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route('/log/<userid>/<category>/<fileid>', methods=['POST'])
@requires_auth
def log_api_stub(userid, category, fileid):
    try:
        assert userid == '31'
        assert category == 'device_vital'
        assert 'test.vit' in fileid
        request.files.get('test_dir/test.vit').read().decode('utf-8') == '42'
        return "OK"
    except:
        import traceback
        print(fileid)
        print(traceback.format_exc())


@app.route('/user/<userid>')
def user_profile_stub(userid):
    try:
        assert userid == '31'
        return "OK"
    except:
        import traceback
        print(traceback.format_exc())


def test_runner():
    import time
    time.sleep(2.0)
#    print(r, r.status_code, r.text, r.encoding)
    conf = uploader.Conf()
    proxy = uploader.APIProxy(conf.base_url, conf.port)
    uploader.Uploader(conf, proxy).execute()


def test_conf():
    #-u 31 -d test_dir -c 13
    conf = uploader.Conf()
    print(conf)
    sys.exit(0)

if __name__ == '__main__':
    #test_conf()
    p = multiprocessing.Process(target=test_runner)
    p.start()
    p1 = multiprocessing.Process(target=app.run)
    p1.start()
    p.join()
    p1.terminate()