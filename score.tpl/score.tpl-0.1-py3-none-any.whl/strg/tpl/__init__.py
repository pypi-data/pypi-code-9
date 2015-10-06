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

import jinja2.ext
import os
from pyramid.events import BeforeRender
from pyramid.settings import asbool

import logging
log = logging.getLogger(__name__)


def rootdir(request):
    return request.registry.settings['tpl.root']


def virtjs(*args, **kwargs):
    from .js import virtjs as v
    global virtjs
    virtjs = v
    virtjs(*args, **kwargs)


def virtcss(*args, **kwargs):
    from .css import virtcss as v
    global virtcss
    virtcss = v
    virtcss(*args, **kwargs)


class FilenameEmbedder(jinja2.ext.Extension):

    def preprocess(self, source, name, filename=None):
        source = self._preprocess(source, name, filename)
        return super().preprocess(source, name, filename)

    def _preprocess(self, source, name, fielname):
        if not name.endswith('.jinja2'):
            return source
        if '.' in name[:-7] and not name.endswith('.html.jinja2'):
            return source
        location = name
        if filename is not None:
            location = '%s | %s' % (name, filename)
        start = '<!-- START %s -->\n\n' % location
        end = '\n\n<!-- END %s -->' % location
        return start + source + end


def register_globals(event):
    import strg.tpl as tpl
    event['js'] = tpl.js.TagGenerator(event['request'])
    event['css'] = tpl.css.TagGenerator(event['request'])
    event['icon'] = tpl.icons.TagGenerator(event['request'])


def render(file, context):
    """
    Renders given jinja *file* with the provided *context*.
    """
    assert configuration is not None
    global jinja2_environment
    if jinja2_environment is None:
        jinja2_environment = configuration.get_jinja2_environment()
        if jinja2_environment.bytecode_cache:
            jinja2_environment.bytecode_cache.clear()
    template = jinja2_environment.get_template(file)
    return template.render(context)

configuration = None
jinja2_environment = None

def configure(settings, config):
    from . import css, js
    global configuration
    configuration = config
    # jinja2
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path(settings['tpl.root'])
    config.add_subscriber(register_globals, BeforeRender)
    config.add_jinja2_extension('jinja2.ext.i18n')
    try:
        if asbool(settings['tpl.embedpaths']):
            config.add_jinja2_extension(FilenameEmbedder)
    except KeyError:
        pass
    # add renderers
    config.add_renderer('.css', css.Renderer)
    config.add_renderer('.scss', css.Renderer)
    config.add_renderer('.js', js.Renderer)
    # add css routes
    config.add_route('css/icons/single', '/icons.css')
    config.add_route('css/icons/combined', '/icons-combined.css')
    config.add_route('css/single', r'/css/{path:.*\.css$}')
    config.add_route('css/combined', '/combined.css')
    # add js routes
    config.add_route('js/single/api', '/js/api.js')
    config.add_route('js/single', '/js/{path:.*\.js$}')
    config.add_route('js/combined', '/combined.js')
    # add icons routes
    config.add_route('icons/single/svg', r'/icon/{path:.*\.svg$}')
    config.add_route('icons/single/png', r'/icon/{path:.*\.png$}')
    config.add_route('icons/combined/svg', r'/icons.svg')
    config.add_route('icons/combined/png', r'/icons.png')
    # clear caches
    def clear(key):
        if key not in settings:
            return
        for root, dirs, files in os.walk(settings[key], topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
    clear('js.cachedir')
    clear('css.cachedir')
    clear('icons.cachedir')
    # register views
    config.scan('strg.tpl')

