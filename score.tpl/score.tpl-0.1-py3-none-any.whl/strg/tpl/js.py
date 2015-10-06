# Copyright © 2015 STRG.AT GmbH, Vienna, Austria
#
# This file is part of the The SCORE Framework.
#
# The SCORE Framework and all its parts are free software: you can redistribute
# them and/or modify them under the terms of the GNU Lesser General Public
# License version 3 as published by the Free Software Foundation which is in the
# file named COPYING.LESSER.txt.
#
# The SCORE Framework and all its parts are distributed without any WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. For more details see the GNU Lesser General Public
# License.
#
# If you have not received a copy of the GNU Lesser General Public License see
# http://www.gnu.org/licenses/.
#
# The License-Agreement realised between you as Licensee and STRG.AT GmbH as
# Licenser including the issue of its valid conclusion and its pre- and
# post-contractual effects is governed by the laws of Austria. Any disputes
# concerning this License-Agreement including the issue of its valid conclusion
# and its pre- and post-contractual effects are exclusively decided by the
# competent court, in whose district STRG.AT GmbH has its registered seat, at
# the discretion of STRG.AT GmbH also the competent court, in whose district the
# Licensee has his registered seat, an establishment or assets.

from jinja2 import Markup
import os
from pyramid.renderers import render
from pyramid.settings import asbool
from pyramid.view import view_config
import slimit
import strg.tpl as tpl

import logging
log = logging.getLogger(__name__)

def rootdir(request):
    """
    Returns the root directory of all javascript files.
    """
    return os.path.join(tpl.rootdir(request), 'js')


def minify(js):
    """
    Minifies javascript.
    """
    return slimit.minify(js)


def response(request, js):
    """
    Returns a pyramid response object containing the given javascript. The
    *js* will be minified (via :func:`.minify`) if the configuration value
    ``js.minify`` evaluates to `True`.
    """
    if 'js.minify' in request.registry.settings and \
            asbool(request.registry.settings['js.minify']):
        js = minify(js)
    request.response.content_encoding = 'UTF-8'
    request.response.content_type = 'application/javascript; charset=UTF-8'
    request.response.text = js
    return request.response


def files(request):
    """
    Provides a list of all js files found in the js root folder. This will
    not return any files starting with an underscore. These can be used for
    IE-specific scripts, for example.
    """
    root = rootdir(request)
    jsfiles = []
    for parent, _, files in os.walk(root):
        for file in files:
            if file.endswith('.js'):
                path = os.path.relpath(os.path.join(parent, file), root)
                if os.path.basename(file) in ('require.js', 'globals.js'):
                    jsfiles.insert(0, path)
                else:
                    jsfiles.append(path)
    for f in virtfiles:
        if f not in jsfiles:
            jsfiles.append(f)
    return jsfiles


virtfiles = {}
def virtjs(name=None):
    """
    Registers a virtual javascript file.
    """
    global virtfiles
    if name is not None:
        assert name.endswith('.js')
    def outer(inner):
        nonlocal name
        if name is None:
            name = '%s.js' % inner.__name__
        assert name not in virtfiles
        virtfiles[name] = inner
        return inner
    return outer

@virtjs('require.js')
def x(request):
    return '/* contents of require.js */'

@virtjs('globals.js')
def x(request):
    return '/* contents of globals.js */'

def combining(request):
    try:
        return asbool(request.registry.settings['js.combine'])
    except KeyError:
        return True


@view_config(route_name='js/single')
def js_single(request):
    js = render(request.matchdict['path'], {}, request)
    return response(request, js)


@view_config(route_name='js/combined')
def js_combined(request):
    js = ''
    for file in files(request):
        if os.path.basename(file[0]) == '_':
            continue
        js += '\n\n/* %s */\n' % file
        js += render(file, {}, request)
    return response(request, js[2:])


class TagGenerator:
    """
    This is a helper class for use in jinja-templates. You can use it to
    generate a ``script``-tag to all required js files, or even a single
    js file::

        <head>
            {{ js }}
            <!--[if IE]>
                {{ js('_ie_crutch.js') }}
            <![endif]-->
        </head>
    """

    def __init__(self, request):
        self.request = request

    def __str__(self):
        return self.__call__()

    def __call__(self):
        """
        Returns all requested ``script``-tags as jinja-Markup.
        """
        tag = '<script src="%s"></script>'
        if combining(self.request):
            return Markup(tag % self.request.route_url('js/combined'))
        links = []
        for file in files(self.request):
            links.append(tag % self.request.route_url('js/single', path=file))
        return Markup('\n'.join(links))


class Renderer:
    """
    A `pyramid renderer <pyramid:adding_and_overriding_renderers>` that
    renders ``js`` files. Will run the files through jinja, too.
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
        if os.path.isfile(path):
            js = tpl.render(path, system)
            if self.info.name == 'require.js':
                js += 'require.config({baseUrl: "%s"});' % system['request'].route_url('js/single', path='')
        else:
            assert self.info.name in virtfiles
            js = virtfiles[self.info.name](system)
        return js

