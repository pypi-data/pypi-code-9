__author__ = 'dpepper'
__version__ = "0.1.0"


import os
import imp
import json
from bson import json_util
import urllib
import flask


def generate_urls(app, src_dir, base_url, default_methods=['GET'], auth_fn=None):
    assert base_url.startswith('/')
    base_url = base_url.rstrip('/')

    if os.path.isdir(src_dir):
        src_dir = os.path.abspath(src_dir)
    else:
        src_dir = '%s/%s' % (app.config['ROOT_PATH'], src_dir)

    assert os.path.isdir(src_dir)
    assert src_dir.startswith(app.config['ROOT_PATH'])

    def generate_view_fn(get_fn, post_fn):
        def view_fn(*args, **kwargs):
            if flask.request.method == 'POST':
                res = view_fn.post_fn(*args, **kwargs)
            else:
                # GET
                res = view_fn.get_fn(*args, **kwargs)

            if None == res:
                res = ('', 204)  # Empty Response Code
            elif type(res) in [list, dict]:
                # auto-package results into json
                res = flask.Response(
                    json.dumps(res, default=json_util.default),
                    mimetype='application/json',
                )

            return res
        view_fn.get_fn = get_fn
        view_fn.post_fn = post_fn

        return view_fn

    paths = {}
    for path, subdirs, filenames in os.walk(src_dir):
        filenames = [f for f in filenames if f.endswith('.py')]
        for filename in filenames:
            if filename == '__init__.py':
                continue

            mod_name = '%s/%s' % (path[len(app.config['ROOT_PATH']):], filename[:-3])
            mod_path = os.path.abspath(path + '/' + filename)
            module = imp.load_source(mod_name, mod_path)

            defaults = getattr(module, 'DEFAULTS', {})
            public_view = getattr(module, 'PUBLIC', False)

            get_fn = getattr(module, 'get', None)
            post_fn = getattr(module, 'post', None)
            view_fn = getattr(module, 'view', None)

            if not any([view_fn, get_fn, post_fn]):
                raise Exception('endpoint missing magic view() or get()/post() functions: ' + mod_path)

            if view_fn and (get_fn or post_fn):
                raise Exception('endpoints can have either view() or get()/post() but not both: ' + mod_path)

            if view_fn:
                if not callable(view_fn):
                    raise Exception('invalid view function: %s' % mod_path)
            else:
                view_fn = generate_view_fn(get_fn, post_fn)

            if not public_view:
                view_fn = auth_fn(view_fn)

            # determine which methods to use for this endpoint
            methods = set(getattr(module, 'METHODS', []))

            if get_fn:
                methods.add('GET')
            if post_fn:
                methods.add('POST')

            methods = methods or default_methods

            if hasattr(module, 'PATH'):
                url_paths = [getattr(module, 'PATH')]
            elif hasattr(module, 'PATHS'):
                url_paths = getattr(module, 'PATHS')
            else:
                # determine this endpoint's url, based on it's path
                # prefix = '%s/%s' % (base_url, path[len(src_dir):])
                url = '%s/%s/%s' % (
                    base_url,
                    path[len(src_dir):],
                    filename[:-3]
                )
                url = url.replace('//', '/')
                url_paths = [url]

            for url in url_paths:
                app.add_url_rule(
                    url,
                    view_func=view_fn,
                    endpoint=mod_name,
                    methods=methods,
                    defaults=defaults
                )
                paths[url] = mod_name


def list_routes(app):
    output = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint == 'static':
            continue

        line = urllib.unquote("{:30s}   {}".format(rule.rule, rule.endpoint))
        if len(line) > 70:
            line = line[:70] + '...'
        output.append(line)

    output = sorted(output)
    return "\n".join(output)
