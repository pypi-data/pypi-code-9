import csscompressor
from jinja2 import Markup, Template
import os
from pyramid.renderers import render
from pyramid.settings import asbool
from pyramid.view import view_config
import scss
import strg.tpl as tpl

import logging
log = logging.getLogger(__name__)


scss.config.DEBUG = True
scss.config.STYLE = 'expanded'


def rootdir(request):
    """
    Returns the root directory of all css files.
    """
    return os.path.join(tpl.rootdir(request), 'css')


def minify(css):
    """
    Minifies a css string. The *css* must be a valid css string, i.e. it must
    not contain scss or sass or any other format.
    """
    return csscompressor.compress(css)


def response(request, css):
    """
    Returns a pyramid response object containing the given css string. The
    *css* will be minified (via :func:`.minify`) if the configuration value
    ``css.minify`` evaluates to `True`.
    """
    if 'css.minify' in request.registry.settings and \
            asbool(request.registry.settings['css.minify']):
        css = minify(css)
    request.response.content_encoding = 'UTF-8'
    request.response.content_type = 'text/css; charset=UTF-8'
    request.response.text = css
    return request.response


def combining(request):
    try:
        return asbool(request.registry.settings['css.combine'])
    except KeyError:
        return True


virtfiles = {}
def virtcss(name=None):
    """
    Registers a virtual css file.
    """
    global virtfiles
    if name is not None:
        assert name.endswith('.css')
    def outer(inner):
        nonlocal name
        if name is None:
            name = '%s.css' % inner.__name__
        assert name not in virtfiles
        virtfiles[name] = inner
        return inner
    return outer


def files(request):
    """
    Provides a list of all css files found in the css root folder. This will
    not return any files starting with an underscore. These can be used for
    IE-specific styles, for example.
    """
    root = rootdir(request)
    cssfiles = []
    for parent, _, files in os.walk(root, followlinks=True):
        for file in files:
            if file.endswith('.css') or file.endswith('.scss'):
                path = os.path.relpath(os.path.join(parent, file), root)
                if file == 'reset.css':
                    cssfiles.insert(0, path)
                else:
                    cssfiles.append(path)
    for f in virtfiles:
        if f not in cssfiles:
            cssfiles.append(f)
    return cssfiles


@view_config(route_name='css/single')
def css_single(request):
    """
    Returns a single css file.
    """
    if request.matchdict is None or 'path' not in request.matchdict:
        request.response.status = 404
        return request.response
    css = render(request.matchdict['path'], {}, request)
    return response(request, css)


@view_config(route_name='css/combined')
def css_all(request):
    """
    Returns all css files in a single response. The files will be separated
    by css-comments containing the file names.
    """
    css = ''
    for file in files(request):
        if os.path.basename(file[0]) == '_':
            continue
        css += '\n\n/* %s */\n' % file
        css += render(file, {}, request)
    return response(request, css[2:])


class TagGenerator:
    """
    This is a helper class for use in jinja-templates. You can use it to
    generate a ``link``-tag to all required css files, or even a single
    css file::

        <head>
            {{ css }}
            <!--[if IE]>
                {{ css('_ie_crutch.css') }}
            <![endif]-->
        </head>
    """

    def __init__(self, request):
        self.request = request

    def __str__(self):
        return self.__call__()

    def __call__(self, file):
        """
        Returns all requested ``style``-tags as jinja-Markup.
        """
        tag = '<link rel="stylesheet" href="%s" type="text/css">'
        if file:
            if path.endswith('.scss'):
                path = path[:-4] + 'css'
            return Markup(tag % self.request.route_url('css/single'), path=path)
        if combining(self.request):
            return Markup(tag % self.request.route_url('css/all'))
        tags = []
        for path in files(self.request):
            if os.path.basename(path[0]) == '_':
                continue
            if path.endswith('.scss'):
                path = path[:-4] + 'css'
            tags.append(tag % self.request.route_url('css/single', path=path))
        return Markup('\n'.join(tags))


class Renderer:
    """
    A `pyramid renderer <pyramid:adding_and_overriding_renderers>` that
    renders ``css`` and ``scss`` files. Will run all results through jinja,
    too.
    """
    def __init__(self, info):
        """
        From the pyramid documentation:

            Constructor: info will be an object having the
            following attributes: name (the renderer name), package
            (the package that was 'current' at the time the
            renderer was registered), type (the renderer type
            name), registry (the current application registry) and
            settings (the deployment settings dictionary).
        """
        self.info = info

    def __call__(self, value, system):
        """
        From the pyramid documentation:

            Call the renderer implementation with the value
            and the system value passed in as arguments and return
            the result (a string or unicode object).  The value is
            the return value of a view.  The system value is a
            dictionary containing available system values
            (e.g. view, context, and request).
        """
        path = os.path.join(rootdir(system['request']), self.info.name)
        if self.info.name.endswith('.css'):
            if os.path.isfile(path):
                return tpl.render(path, system)
            if self.info.name in virtfiles:
                return virtfiles[self.info.name](system['request'])
            path = path[:-3] + 'scss'
            assert os.path.isfile(path)
        else:
            assert self.info.name.endswith('.scss')
            assert os.path.isfile(path)
        def uncached():
            rendered = tpl.render(path, system)
            compiler = scss.Scss(search_paths=[rootdir(system['request'])])
            return compiler.compile(rendered)
        try:
            cachedir = system['request'].registry.settings['css.cachedir']
        except KeyError:
            return uncached()
        if not cachedir:
            return uncached()
        cachefile = os.path.join(cachedir, self.info.name)
        if not os.path.isfile(cachefile) or os.path.getmtime(path) >= os.path.getmtime(cachefile):
            os.makedirs(os.path.dirname(cachefile), exist_ok=True)
            open(cachefile, 'w').write(uncached())
        return open(cachefile, 'r').read()

