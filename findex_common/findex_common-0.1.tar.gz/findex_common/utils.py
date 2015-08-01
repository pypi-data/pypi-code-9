from bottle import request
import cgi,urllib
import bytes2human as bytes2human
from datetime import datetime


class DataObjectManipulation():
    def __init__(self, dataobject):
        self.dataobject = dataobject

    def dictionize(self, dataobject):
        d = {}
        for attr in [a for a in dir(dataobject) if not a.startswith('__') and not a.startswith('_')]:
            d[attr] = getattr(dataobject, attr)
        return d

    def sanitize(self, dataobject):
        for attr in [a for a in dir(dataobject) if not a.startswith('__') and not a.startswith('_')]:
            get_attr = getattr(dataobject, attr)

            if isinstance(get_attr, str) or isinstance(get_attr, unicode):
                if get_attr == 'None' or get_attr == '':
                    setattr(dataobject, attr, None)
        return dataobject

    def sanitize_userinput(self, dataobject):
        if not isinstance(dataobject, dict):
            for attr in [a for a in dir(dataobject) if not a.startswith('__') and not a.startswith('_')]:
                a = getattr(dataobject, attr)
        else:
            data = {}

            def san(inp):
                    cgi.escape(urllib.quote_plus(inp))

            for k, v in dataobject.iteritems():
                if isinstance(v, list):
                    for i in range(0, len(v)):
                        dataobject[k] = san(v[i])

        return dataobject

    def humanize(self, humansizes=False, humandates=False, dateformat=None, humanpath=False, humanfile=False):
        for attr in [a for a in dir(self.dataobject) if not a.startswith('_')]:
            if humandates:
                get_attr = getattr(self.dataobject, attr)
                format = '%d %b %Y %H:%M' if not dateformat else dateformat

                if isinstance(get_attr, datetime):
                    setattr(self.dataobject, '%s_human' % attr, get_attr.strftime(format))

            if humansizes:
                get_attr = getattr(self.dataobject, attr)
                isnum = False

                if isinstance(get_attr, int):
                    isnum = True
                elif isinstance(get_attr, long):
                    isnum = True

                if isnum:
                    tokens = ['filesize', 'file_size', 'bytes', 'total_size', 'size_files']
                    if attr in tokens:
                        setattr(self.dataobject, attr + '_human', bytes2human.bytes2human(get_attr))

            if humanpath or humanfile:
                get_attr = getattr(self.dataobject, attr)

                if isinstance(get_attr, str) or isinstance(get_attr, unicode):
                    tokens = ['file_path', 'file_name']
                    if attr in tokens:
                        setattr(self.dataobject, attr + '_human', urllib.unquote_plus(get_attr))

        return self.dataobject


class Types():
    def is_int(self, x):
        try:
            if isinstance(x, int):
                return x
            return int(x)
        except Exception as e:
            return

    def is_float(self, x):
        try:
            if isinstance(x, float):
                return x
            return float(x)
        except Exception as e:
            return


class ArgValidate():
    def __init__(self):
        self._types = Types()
        self._uri = 'post'

    def post_get(self, name, default=''):
        return request.POST.get(name, default)

    def get_get(self, name):
        if name in request.params.dict:
            if request.params.dict[name]:
                if request.params.dict[name][0]:
                    return request.params.dict[name][0]

    def verify_args(self, args, method):
        data = {}

        for k, v in args.iteritems():

            if method.lower() == 'get':
                result = self.get_get(k)
            else:
                result = self.post_get(k)

            if result:
                if v == 'float':
                    if self._types.is_float(result):
                        data[k] = float(result)
                        continue
                    else:
                        return '%s was not of type %s' % (result, v)
                elif v == 'int':
                    result = self._types.is_int(result)

                    if result:
                        data[k] = int(result)
                    elif result == 0 and isinstance(result, int):
                        data[k] = int(result)
                    else:
                        return '%s was not of type %s' % (result, v)
                else:
                    data[k] = result
            else:
                return '%s not found as arg' % k

        return data