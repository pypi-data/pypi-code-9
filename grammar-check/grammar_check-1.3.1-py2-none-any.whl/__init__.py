# -*- coding: utf-8 -*-

# © 2012 spirit <hiddenspirit@gmail.com>
# © 2013-2014 Steven Myint
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

u"""LanguageTool through server mode."""

from __future__ import with_statement
from __future__ import absolute_import
import atexit
import glob
import httplib
import locale
import os
import re
import socket
import sys
import urllib2, urllib, urlparse
import urllib2, urllib
from collections import OrderedDict
from functools import total_ordering
from weakref import WeakValueDictionary

try:
    from xml.etree import cElementTree as ElementTree
except ImportError:
    from xml.etree import ElementTree

from .backports import subprocess
from .which import which


__version__ = u'1.3.1'


__all__ = [u'LanguageTool', u'Error', u'get_languages', u'correct', u'get_version',
           u'get_directory', u'set_directory']

JAR_NAMES = [
    u'languagetool-server.jar',
    u'languagetool-standalone*.jar',  # 2.1
    u'LanguageTool.jar',
    u'LanguageTool.uno.jar'
]
FAILSAFE_LANGUAGE = u'en'

# https://mail.python.org/pipermail/python-dev/2011-July/112551.html
USE_URLOPEN_RESOURCE_WARNING_FIX = (3, 1) < sys.version_info < (3, 4)

if os.name == u'nt':
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
else:
    startupinfo = None

cache = {}


class Error(Exception):

    u"""LanguageTool Error."""


class ServerError(Error):
    pass


class JavaError(Error):
    pass


class PathError(Error):
    pass


def get_replacement_list(string, sep=u'#'):
    if isinstance(string, list):
        return string
    return string.split(sep) if string else []


def auto_type(string):
    try:
        return int(string)
    except ValueError:
        try:
            return float(string)
        except ValueError:
            return string


class Match(object):

    u"""Hold information about where a rule matches text."""
    _SLOTS = OrderedDict([
        (u'fromy', int), (u'fromx', int), (u'toy', int), (u'tox', int),
        (u'ruleId', unicode), (u'subId', unicode), (u'msg', unicode),
        (u'replacements', get_replacement_list),
        (u'context', unicode), (u'contextoffset', int),
        (u'offset', int), (u'errorlength', int),
        (u'url', unicode), (u'category', unicode), (u'locqualityissuetype', unicode),
    ])

    def __init__(self, attrib):
        for k, v in attrib.items():
            setattr(self, k, v)

    def __repr__(self):
        def _ordered_dict_repr():
            slots = list(self._SLOTS)
            slots += list(set(self.__dict__).difference(slots))
            attrs = [slot for slot in slots
                     if slot in self.__dict__ and not slot.startswith(u'_')]
            return u'{{{}}}'.format(
                u', '.join([
                    u'{!r}: {!r}'.format(attr, getattr(self, attr))
                    for attr in attrs
                ])
            )

        return u'{}({})'.format(self.__class__.__name__, _ordered_dict_repr())

    def __str__(self):
        ruleId = self.ruleId
        if self.subId is not None:
            ruleId += u'[{}]'.format(self.subId)
        s = u'Line {}, column {}, Rule ID: {}'.format(
            self.fromy + 1, self.fromx + 1, ruleId)
        if self.msg:
            s += u'\nMessage: {}'.format(self.msg)
        if self.replacements:
            s += u'\nSuggestion: {}'.format(u'; '.join(self.replacements))
        s += u'\n{}\n{}'.format(
            self.context, u' ' * self.contextoffset + u'^' * self.errorlength
        )
        return s

    def __eq__(self, other):
        return list(self) == list(other)

    def __lt__(self, other):
        return list(self) < list(other)

    def __iter__(self):
        return iter(getattr(self, attr) for attr in self._SLOTS)

    def __setattr__(self, name, value):
        try:
            value = self._SLOTS[name](value)
        except KeyError:
            value = auto_type(value)
        super(Match, self).__setattr__(name, value)

    def __getattr__(self, name):
        if name not in self._SLOTS:
            raise AttributeError(u'{!r} object has no attribute {!r}'
                                 .format(self.__class__.__name__, name))


Match = total_ordering(Match)

class LanguageTool(object):

    u"""Main class used for checking text against different rules."""
    _HOST = socket.gethostbyname(u'localhost')
    _MIN_PORT = 8081
    _MAX_PORT = 8083
    _TIMEOUT = 60

    _port = _MIN_PORT
    _server = None
    _instances = WeakValueDictionary()
    _PORT_RE = re.compile(ur"(?:https?://.*:|port\s+)(\d+)", re.I)

    def __init__(self, language=None, motherTongue=None):
        if not self._server_is_alive():
            self._start_server_on_free_port()
        if language is None:
            try:
                language = get_locale_language()
            except ValueError:
                language = FAILSAFE_LANGUAGE
        self._language = LanguageTag(language)
        self.motherTongue = motherTongue
        # spell check rules are disabled by default
        self.disabled = set([u'HUNSPELL_RULE', u'HUNSPELL_NO_SUGGEST_RULE', u'YOUR_NN', u'TRY_AND', u'PRP_PAST_PART',
                u'MORFOLOGIK_RULE_' + self.language.replace(u'-', u'_').upper()])
        self.enabled = set()
        self._instances[id(self)] = self

    def __del__(self):
        if not self._instances and self._server_is_alive():
            #self._terminate_server()
            pass

    def __repr__(self):
        return u'{}(language={!r}, motherTongue={!r})'.format(
            self.__class__.__name__, self.language, self.motherTongue)

    @property
    def language(self):
        u"""The language to be used."""
        return self._language

    @language.setter
    def language(self, language):
        self._language = LanguageTag(language)
        self.disabled.clear()
        self.enabled.clear()

    @property
    def motherTongue(self):
        u"""The user's mother tongue or None.

        The mother tongue may also be used as a source language for
        checking bilingual texts.

        """
        return self._motherTongue

    @motherTongue.setter
    def motherTongue(self, motherTongue):
        self._motherTongue = (None if motherTongue is None
                              else LanguageTag(motherTongue))

    @property
    def _spell_checking_rules(self):
        return set([u'HUNSPELL_RULE', u'HUNSPELL_NO_SUGGEST_RULE', 
                u'MORFOLOGIK_RULE_' + self.language.replace(u'-', u'_').upper()])

    def check(self, text, srctext=None):
        u"""Match text against enabled rules."""
        root = self._get_root(self._url, self._encode(text, srctext))
        return [Match(e.attrib) for e in root if e.tag == u'error']

    def _check_api(self, text, srctext=None):
        u"""Match text against enabled rules (result in XML format)."""
        root = self._get_root(self._url, self._encode(text, srctext))
        return ('<?xml version="1.0" encoding="UTF-8"?>\n' +
                ElementTree.tostring(root) + "\n")

    def _encode(self, text, srctext=None):
        params = {u'language': self.language, u'text': text.encode(u'utf-8')}
        if srctext is not None:
            params[u'srctext'] = srctext.encode(u'utf-8')
        if self.motherTongue is not None:
            params[u'motherTongue'] = self.motherTongue
        if self.disabled:
            params[u'disabled'] = u','.join(self.disabled)
        if self.enabled:
            params[u'enabled'] = u','.join(self.enabled)
        return urllib.urlencode(params).encode()

    def correct(self, text, srctext=None):
        u"""Automatically apply suggestions to the text."""
        return correct(text, self.check(text, srctext))

    def enable_spellchecking(self):
        u"""Enable spell-checking rules."""
        self.disabled.difference_update(self._spell_checking_rules)

    def disable_spellchecking(self):
        u"""Disable spell-checking rules."""
        self.disabled.update(self._spell_checking_rules)

    @classmethod
    def _get_languages(cls):
        u"""Get supported languages (by querying the server)."""
        if not cls._server_is_alive():
            cls._start_server_on_free_port()
        url = urlparse.urljoin(cls._url, u'Languages')
        languages = set()
        for e in cls._get_root(url, num_tries=1):
            languages.add(e.get(u'abbr'))
            languages.add(e.get(u'abbrWithVariant'))
        return languages

    @classmethod
    def _get_attrib(cls):
        u"""Get matches element attributes."""
        if not cls._server_is_alive():
            cls._start_server_on_free_port()
        params = {u'language': FAILSAFE_LANGUAGE, u'text': u''}
        data = urllib.urlencode(params).encode()
        root = cls._get_root(cls._url, data, num_tries=1)
        return root.attrib

    @classmethod
    def _get_root(cls, url, data=None, num_tries=2):
        for n in xrange(num_tries):
            try:
                with urlopen(url, data, cls._TIMEOUT) as f:
                    return ElementTree.parse(f).getroot()
            except (IOError, httplib.HTTPException), e:
                cls._terminate_server()
                cls._start_server()
                if n + 1 >= num_tries:
                    raise Error(u'{}: {}'.format(cls._url, e))

    @classmethod
    def _start_server_on_free_port(cls):
        while True:
            cls._url = u'http://{}:{}'.format(cls._HOST, cls._port)
            try:
                cls._start_server()
                break
            except ServerError:
                if cls._MIN_PORT <= cls._port < cls._MAX_PORT:
                    cls._port += 1
                else:
                    raise

    @classmethod
    def _start_server(cls):
        err = None
        try:
            server_cmd = get_server_cmd(cls._port)
        except PathError, e:
            # Can't find path to LanguageTool.
            err = e
        else:
            # Need to PIPE all handles: http://bugs.python.org/issue3905
            cls._server = subprocess.Popen(
                server_cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                startupinfo=startupinfo
            )
            # Python 2.7 compatibility
            # for line in cls._server.stdout:
            match = None
            while True:
                line = cls._server.stdout.readline()
                if not line:
                    break
                match = cls._PORT_RE.search(line)
                if match:
                    port = int(match.group(1))
                    if port != cls._port:
                        raise Error(u'requested port {}, but got {}'
                                    .format(cls._port, port))
                    break
            if not match:
                cls._terminate_server()
                err_msg = cls._server.communicate()[1].strip()
                cls._server = None
                match = cls._PORT_RE.search(err_msg)
                if not match:
                    raise Error(err_msg)
                port = int(match.group(1))
                if port != cls._port:
                    raise Error(err_msg)
        if not cls._server:
            # Couldn't start the server, so maybe there is already one running.
            params = {u'language': FAILSAFE_LANGUAGE, u'text': u''}
            data = urllib.urlencode(params).encode()
            try:
                with urlopen(cls._url, data, cls._TIMEOUT) as f:
                    tree = ElementTree.parse(f)
            except (IOError, httplib.HTTPException), e:
                if err:
                    raise err
                raise ServerError(u'{}: {}'.format(cls._url, e))
            root = tree.getroot()

            # LanguageTool 1.9+
            if root.get(u'software') != u'LanguageTool':
                raise ServerError(u'unexpected software from {}: {!r}'
                                  .format(cls._url, root.get(u'software')))

    @classmethod
    def _server_is_alive(cls):
        return cls._server and cls._server.poll() is None

    @classmethod
    def _terminate_server(cls):
        try:
            cls._server.terminate()
        except OSError:
            pass


class LanguageTag(unicode):

    u"""Language tag supported by LanguageTool."""
    _LANGUAGE_RE = re.compile(ur"^([a-z]{2,3})(?:[_-]([a-z]{2}))?$", re.I)

    def __new__(cls, tag):
        # Can't use super() here because of 3to2.
        return unicode.__new__(cls, cls._normalize(tag))

    def __eq__(self, other):
        try:
            other = self._normalize(other)
        except ValueError:
            pass
        return unicode(self) == other

    def __lt__(self, other):
        try:
            other = self._normalize(other)
        except ValueError:
            pass
        return unicode(self) < other

    @classmethod
    def _normalize(cls, tag):
        if not tag:
            raise ValueError(u'empty language tag')
        languages = dict((language.lower().replace(u'-', u'_'), language)
                     for language in get_languages())
        try:
            return languages[tag.lower().replace(u'-', u'_')]
        except KeyError:
            try:
                return languages[cls._LANGUAGE_RE.match(tag).group(1).lower()]
            except (KeyError, AttributeError):
                raise ValueError(u'unsupported language: {!r}'.format(tag))


LanguageTag = total_ordering(LanguageTag)

def correct(text, matches):
    u"""Automatically apply suggestions to the text."""
    ltext = list(text)
    matches = [match for match in matches if match.replacements]
    errors = [ltext[match.offset:match.offset + match.errorlength]
              for match in matches]
    correct_offset = 0
    for n, match in enumerate(matches):
        frompos, topos = (correct_offset + match.offset,
                          correct_offset + match.offset + match.errorlength)
        if ltext[frompos:topos] != errors[n]:
            continue
        repl = match.replacements[0]
        ltext[frompos:topos] = list(repl)
        correct_offset += len(repl) - len(errors[n])
    return u''.join(ltext)


def _get_attrib():
    try:
        attrib = cache[u'attrib']
    except KeyError:
        attrib = LanguageTool._get_attrib()
        cache[u'attrib'] = attrib
    return attrib


def get_version():
    u"""Get LanguageTool version."""
    version = _get_attrib().get(u'version')
    if not version:
        match = re.search(ur"LanguageTool-?.*?(\S+)$", get_directory())
        if match:
            version = match.group(1)
    return version


def get_build_date():
    u"""Get LanguageTool build date."""
    return _get_attrib().get(u'buildDate')


def get_languages():
    u"""Get supported languages."""
    try:
        languages = cache[u'languages']
    except KeyError:
        languages = LanguageTool._get_languages()
        cache[u'languages'] = languages
    return languages


def get_directory():
    u"""Get LanguageTool directory."""
    try:
        language_check_dir = cache[u'language_check_dir']
    except KeyError:
        def version_key(string):
            return [int(e) if e.isdigit() else e
                    for e in re.split(ur"(\d+)", string)]

        def get_lt_dir(base_dir):
            paths = [
                path for path in
                glob.glob(os.path.join(base_dir, u'LanguageTool*'))
                if os.path.isdir(path)
            ]
            return max(paths, key=version_key) if paths else None

        base_dir = os.path.dirname(sys.argv[0])
        language_check_dir = get_lt_dir(base_dir)
        if not language_check_dir:
            try:
                base_dir = os.path.dirname(os.path.abspath(__file__))
            except NameError:
                pass
            else:
                language_check_dir = get_lt_dir(base_dir)
            if not language_check_dir:
                raise PathError(u"can't find LanguageTool directory in {!r}"
                                .format(base_dir))
        cache[u'language_check_dir'] = language_check_dir
    return language_check_dir


def set_directory(path=None):
    u"""Set LanguageTool directory."""
    old_path = get_directory()
    terminate_server()
    cache.clear()
    if path:
        cache[u'language_check_dir'] = path
        try:
            get_jar_info()
        except Error:
            cache[u'language_check_dir'] = old_path
            raise


def get_server_cmd(port=None):
    try:
        cmd = cache[u'server_cmd']
    except KeyError:
        java_path, jar_path = get_jar_info()
        cmd = [java_path, u'-cp', jar_path,
               u'org.languagetool.server.HTTPServer']
        cache[u'server_cmd'] = cmd
    return cmd if port is None else cmd + [u'-p', unicode(port)]


def get_jar_info():
    try:
        java_path, jar_path = cache[u'jar_info']
    except KeyError:
        java_path = which(u'java')
        if not java_path:
            raise JavaError(u"can't find Java")
        dir_name = get_directory()
        jar_path = None
        for jar_name in JAR_NAMES:
            for jar_path in glob.glob(os.path.join(dir_name, jar_name)):
                if os.path.isfile(jar_path):
                    break
            else:
                jar_path = None
            if jar_path:
                break
        else:
            raise PathError(u"can't find languagetool-standalone in {!r}"
                            .format(dir_name))
        cache[u'jar_info'] = java_path, jar_path
    return java_path, jar_path


def get_locale_language():
    u"""Get the language code for the current locale setting."""
    return locale.getlocale()[0] or locale.getdefaultlocale()[0]


@atexit.register
def terminate_server():
    u"""Terminate the server."""
    if LanguageTool._server_is_alive():
        LanguageTool._terminate_server()


if USE_URLOPEN_RESOURCE_WARNING_FIX:
    class ClosingHTTPResponse(httplib.HTTPResponse):

        def __init__(self, sock, *args, **kwargs):
            super(ClosingHTTPResponse, self).__init__(sock, *args, **kwargs)
            self._socket_close = sock.close

        def close(self):
            super(ClosingHTTPResponse, self).close()
            self._socket_close()

    class ClosingHTTPConnection(httplib.HTTPConnection):
        response_class = ClosingHTTPResponse

    class ClosingHTTPHandler(urllib2.HTTPHandler):

        def http_open(self, req):
            return self.do_open(ClosingHTTPConnection, req)

    urlopen = urllib2.build_opener(ClosingHTTPHandler).open

else:
    try:
        urllib.response.addinfourl.__exit__
    except AttributeError:
        from contextlib import closing

        def urlopen(*args, **kwargs):
            return closing(urllib2.urlopen(*args, **kwargs))
    else:
        urlopen = urllib2.urlopen
