"""Miscellaneous utility functions."""

__all__ = [
    'absolute_url',
    'add_global_tmpl_vars',
    'code2html',
    'get_user_id',
    'get_server_name',
    'get_static_content',
    'message_of_the_day',
    'txt2html',
    'wrap_text',
]

import logging
import random
import textwrap

from os.path import join

import cherrypy
from turbogears import config, identity, url
from turbogears.release import version as tg_version
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.styles import get_style_by_name
from pygments.formatters import HtmlFormatter

try:
    from spammcan.rest import HTML
    config.update({'has_docutils': True})
except ImportError:
    config.update({'has_docutils': False})


log = logging.getLogger('spammcan.controllers')
_static_dir = config.get('static_filter.dir', path='/static')


def absolute_url(tgpath='/', params=None, **kw):
    """Returns absolute URL (including schema and host to this server).

    Tries to account for 'Host' header and reverse proxing ('X-Forwarded-Host').

    """

    h = cherrypy.request.headers
    use_xfh = config.get('base_url_filter.use_x_forwarded_host', False)
    if h.get('X-Use-SSL'):
        scheme = 'https'
    else:
        scheme = cherrypy.request.scheme
    base_url = '%s://%s' % (scheme, get_server_name())
    if config.get('base_url_filter.on', False) and not use_xfh:
        base_url = config.get('base_url_filter.base_url').rstrip('/')
    return '%s%s' % (base_url, url(tgpath, params, **kw))

def add_global_tmpl_vars(vars):
    """Add custom global template variables.

    Adds the following variables:

    ``tg.motd`` - The message of the day as a plain string

    """
    vars['motd'] = message_of_the_day()
    vars['abs_url'] = absolute_url
    vars['tg_version'] = tg_version

def code2html(code, format, style=None, cssclass="source", hl_lines=None,
        linenos=False):
    """Syntax highlight given code with Pygments and format as HTML."""
    formatter_options = dict(
        style=style or 'default',
        linenos=linenos,
        cssclass=cssclass,
        lineanchors='L')
    if hl_lines:
        formatter_options['hl_lines'] = hl_lines
    lexer = get_lexer_by_name(format)
    formatter = HtmlFormatter(**formatter_options)
    return highlight(code, lexer, formatter), formatter.get_style_defs(
        '.' + cssclass)

def get_user_id():
    """Return id of current visitor.

    This will be a string with 32-char MD5 hash, which will be retrieved either
    from a request cookie or default to the visit_key of the current identity.

    As a side affect this function sets a response cookie for the user ID
    called 'spammcan_uid' with an expiry time set by the
    'spammcan.uid_cookie_expiry' config setting (defaults to 90 days).

    """
    cookie = cherrypy.request.simple_cookie.get('spammcan_uid')
    log.debug("User ID cookie: %r", cookie)
    if cookie:
        uid = cookie.value
    else:
        uid = identity.current.visit_key
    cherrypy.response.simple_cookie['spammcan_uid'] = uid
    cherrypy.response.simple_cookie['spammcan_uid']['expires'] = config.get(
        'spammcan.uid_cookie_expiry', 3600*24*90)
    return uid

def get_server_name():
    """Return name of the server this application runs on.

    Tries to account for 'Host' header and reverse proxing.

    """
    h = cherrypy.request.headers
    return config.get('server.domain', h.get('X-Forwarded-Host', h['Host']))

def get_static_content(name):
    """Read text file from static directory and convert it to HTML."""
    filename = join(_static_dir, name)
    try:
        fo = open(filename, 'rb')
    except (OSError, IOError):
        text = _(u"Could not read static content resource '%s'.") % name
    else:
        text = fo.read().decode('utf-8')
        fo.close()
    return txt2html(text)

def message_of_the_day(filename='tipoftheday.txt'):
    """Return random message of the day from a text file with one msg per line.
    """
    totd = join(_static_dir, filename)
    return random.choice(filter(None, open(totd).readlines()))

def txt2html(text, use_docutils=True):
    """Try to convert text into HTML with docutils.

    If conversion fails or using docutils is turned off by the configuration,
    return text wrapped in a PRE element with CSS class "plaintext".

    """
    use_docutils = use_docutils and config.get('has_docutils', False)
    if use_docutils:
        try:
            text = HTML(text, report_level=0, initial_header_level=2)
        except Exception, exc:
            log.debug("txt2html failed: %r,", exc)
            use_docutils = False
    return use_docutils and text or '<pre class="plaintext">%s</pre>' % text

def _wrap_line(s, width=100):
    """Wrap single paragraph of text with custom options."""
    return textwrap.wrap(s, width=width, subsequent_indent='  ',
        expand_tabs=True, replace_whitespace=False, break_long_words=False)

def wrap_text(s, width=100):
    """Wrap each paragraph in s with wrap().

    Returns 2-item tuple with a list of line nummers of continuation lines, and
    the wrapped text.

    """
    i = 1; wrapped_lines = []; output= []
    for line in s.splitlines():
        newlines = _wrap_line(line, width) or ['']
        if len(newlines) > 1:
            wrapped_lines.extend(range(i+1,i+len(newlines)))
        i += len(newlines)
        output.extend(newlines)
    return wrapped_lines, "\n".join(output)
