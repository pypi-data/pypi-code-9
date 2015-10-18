# -*- coding: utf-8 -*-
#
# mercurial extension utils: library supporting mercurial extensions
# writing
#
# Copyright (c) 2015 Marcin Kasperski <Marcin.Kasperski@mekk.waw.pl>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. The name of the author may not be used to endorse or promote products
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# See README.txt for more details.

"""Utility functions useful during Mercurial extension writing

Mostly related to configuration processing, path matching and
similar activities. I extracted this module once I noticed a couple
of my extensions need the same or similar functions.
"""

from mercurial.i18n import _

import re
import os
from collections import deque

# pylint: disable=line-too-long,invalid-name

###########################################################################
# Directory matching in various shapes
###########################################################################


def belongs_to_tree(child, parent):
    """Checks whether child lies anywhere inside parent directory tree.

    Child should be absolute path, parent will be tilda expanded and
    converted to absolute path (this convention is caused by typical
    use case, where repo.root is compared against some user-specified
    directory).

    On match, matching parent is returned (it matters if it was
    sanitized).

    >>> belongs_to_tree("/tmp/sub/dir", "/tmp")
    '/tmp'
    >>> belongs_to_tree("/tmp", "/tmp")
    '/tmp'
    >>> belongs_to_tree("/tmp/sub", "/tmp/sub/dir/../..")
    '/tmp'

    On mismatch None is returned.

    >>> belongs_to_tree("/usr/sub", "/tmp")

    Tilda expressions are allowed in parent specification:

    >>> home_work_src = os.path.join(os.environ["HOME"], "work", "src")
    >>> belongs_to_tree(home_work_src, "~/work")
    '/home/marcink/work'
    >>> belongs_to_tree("/home/marcink/devel/webapps", "~marcink/devel")
    '/home/marcink/devel'

    :param child: tested directory (absolute path)
    :param parent: tested parent (will be tilda-expanded, so things
        like ~/work are OK)

    :return: expanded canonicalized parent on match, None on mismatch
    """
    true_parent = os.path.abspath(os.path.expanduser(parent))
    pfx = os.path.commonprefix([child, true_parent])
    return pfx == true_parent and true_parent or None


def belongs_to_tree_group(child, parents):
    """
    Similar to belongs_to_tree, but handles list of candidate parents.

    >>> belongs_to_tree_group("/tmp/sub/dir", ["/bin", "/tmp"])
    '/tmp'
    >>> belongs_to_tree_group("/tmp", ["/tmp"])
    '/tmp'
    >>> belongs_to_tree_group("/tmp/sub/dir", ["/bin", "~/src"])

    Returns longest match if more than one parent matches.

    >>> belongs_to_tree_group("/tmp/sub/dir", ["/tmp","/bin", "/tmp", "/tmp/sub"])
    '/tmp/sub'

    where length is considered after expansion

    >>> belongs_to_tree_group("/home/marcink/src/apps", ["~/src", "/home/marcink"])
    '/home/marcink/src'

    :param child: tested directory (absolute path)
    :param parents: tested parents (list or tuple of directories to
        test, will be tilda-expanded)
    """
    longest_parent = ''
    for parent in parents:
        canon_path = belongs_to_tree(child, parent)
        if canon_path:
            if len(canon_path) > len(longest_parent):
                longest_parent = canon_path
    return longest_parent and longest_parent or None


class DirectoryPattern(object):
    """
    Represents directory name pattern, like ``~/src/{suffix}``, or
    ``/opt/repos/(group)/{suffix}``, and let's match agains such pattern.

    Pattern mini-language:
    - tildas (``~`` and ``~user``) are expanded
    - ``(something)`` matches any part which does not contain directory separator
    - ``{something}`` greedily matches anything, including directory separators

    Constructed pattern can be used to match against, succesfull match extracts
    all marked fragments.

    >>> pat = DirectoryPattern('~/src/{suffix}')
    >>> pat.is_valid()
    True
    >>> pat.search("/opt/repos/abcd")
    >>> pat.search("~/src/repos/in/tree")
    {'suffix': 'repos/in/tree'}
    >>> pat.search("/home/marcink/src/repos/here")
    {'suffix': 'repos/here'}
    >>> pat.search("/home/marcink/src")

    >>> pat = DirectoryPattern('~marcink/devel/(item)')
    >>> pat.search("/opt/repos/abcd")
    >>> pat.search("~/devel/libxuza")
    {'item': 'libxuza'}
    >>> pat.search("~/devel/libs/libxuza")
    >>> pat.search("/home/marcink/devel/webapp")
    {'item': 'webapp'}
    >>> pat.search("/home/marcink/devel")

    >>> pat = DirectoryPattern('/opt/repos/(group)/{suffix}')
    >>> pat.search("/opt/repos/abcd")
    >>> pat.search("/opt/repos/libs/abcd")
    {'group': 'libs', 'suffix': 'abcd'}
    >>> pat.search("/opt/repos/apps/mini/webby")
    {'group': 'apps', 'suffix': 'mini/webby'}

    >>> pat = DirectoryPattern('/opt/repos/(group/{suffix}')
    >>> pat.is_valid()
    False
    >>> pat.search('/opt/repos/some/where')
    """

    # Regexps used during pattern parsing
    _re_pattern_lead = re.compile(r' ^ ([^{}()]*)   ([({]) (.*) $', re.VERBOSE)
    _re_closure = {'{': re.compile(r'^ ([a-zA-Z_]+) [}]    (.*) $', re.VERBOSE),
                   '(': re.compile(r'^ ([a-zA-Z_]+) [)]    (.*) $', re.VERBOSE)}
    # (text inside (braces) or {braces} is restricted as it is used within regexp

    # Regexp snippets used to match escaped parts
    _re_match_snippet = {'{': r'.+',
                         '(': r'[^/\\]+'}

    def __init__(self, pattern_text, ui=None):
        """Parses given pattern. Doesn't raise, in case of invalid patterns
        creates object which does not match anything and warns.

        :param pattern_text: parsed pattern
        :param ui: (optional) mercurial ui object, if given, used for debugging
        """
        self.pattern_text = text = os.path.abspath(os.path.expanduser(pattern_text))
        self._pattern_re = None    # Will stay such if we fail somewhere here

        # Convert pattern to regexp
        rgxp_text = '^'
        while text:
            match = self._re_pattern_lead.search(text)
            if match:
                prefix, open_char, text = match.group(1), match.group(2), match.group(3)
                match = self._re_closure[open_char].search(text)
                if not match:
                    if ui:
                        ui.warn(_("Invalid directory pattern: %s") % pattern_text)
                    return
                group_name, text = match.group(1), match.group(2)
                rgxp_text += re.escape(prefix)
                rgxp_text += '(?P<' + group_name + '>' + self._re_match_snippet[open_char] + ')'
            else:
                rgxp_text += re.escape(text)
                text = ''
        rgxp_text += '$'
        if ui:
            ui.debug(_("Pattern %s translated into regexp %s\n") % (pattern_text, rgxp_text))
        try:
            self._pattern_re = re.compile(rgxp_text)
        except:     # pylint:disable=bare-except
            if ui:
                ui.warn(_("Invalid directory pattern: %s") % pattern_text)

    def is_valid(self):
        """Can be used to check whether object was properly constructed"""
        return bool(self._pattern_re)

    def search(self, tested_path):
        """
        Matches given directory against the pattern.  On match,
        returns dictionary of all named elements.  On mismatch,
        returns None

        :param tested_path: path to check, will be tilda-expanded and
            converted to abspath before comparison
        :return: Dictionary mapping all ``{brace}`` and ``(paren)`` parts to matched
            items
        """
        if not self._pattern_re:
            return
        exp_tested_path = os.path.abspath(os.path.expanduser(tested_path))
        match = self._pattern_re.search(exp_tested_path)
        if match:
            return match.groupdict()
        else:
            return None


###########################################################################
# Text substitution
###########################################################################

class TextFiller(object):
    r'''
    Handle filling patterns like 'some/{thing}/{else}' with values.
    Comparing to standard library ``.format`` offers a bit different
    syntax, related to actual extension-writing problems, and different
    ways of error handling.

    In simplest form, it just replaces any ``{name}`` with value of ``name``, as-is

    >>> tf = TextFiller('{some}/text/to/{fill}')
    >>> tf.fill(some='prefix', fill='suffix')
    'prefix/text/to/suffix'
    >>> tf.fill(some='/ab/c/d', fill='x')
    '/ab/c/d/text/to/x'

    Values can be repeated and unnecessary keys are ignored:

    >>> tf = TextFiller('{some}/text/to/{some}')
    >>> tf.is_valid()
    True
    >>> tf.fill(some='val')
    'val/text/to/val'
    >>> tf.fill(some='ab/c/d', fill='x')
    'ab/c/d/text/to/ab/c/d'

    It is also possible to perform simple substitutions, for example
    ``{name:/=-} takes value of ``name``, replaces all slashes with
    minuses, and fills output with the resulting value

    >>> tf = TextFiller('{prefix:_=___}/goto/{suffix:/=-}')
    >>> tf.fill(prefix='some_prefix', suffix='some/long/suffix')
    'some___prefix/goto/some-long-suffix'

    Substitution can be also used to replace multi-character sequences,
    and replacement can be empty:

    >>> tf = TextFiller('{prefix:/home/=}/docs/{suffix:.txt=.html}')
    >>> tf.fill(prefix='/home/joe', suffix='some/document.txt')
    'joe/docs/some/document.html'

    and chained to replace more than one thing:

    >>> tf = TextFiller(r'/goto/{item:/=-:\=_}/')
    >>> tf.fill(item='this/is/slashy')
    '/goto/this-is-slashy/'
    >>> tf.fill(item=r'this\is\back')
    '/goto/this_is_back/'
    >>> tf.fill(item=r'this/is\mixed')
    '/goto/this-is_mixed/'

    The same parameter can be used in various substitutions:

    >>> tf = TextFiller(r'http://go.to/{item:/=-}, G:{item:/=\}, name: {item}')
    >>> print tf.fill(item='so/me/thing')
    http://go.to/so-me-thing, G:so\me\thing, name: so/me/thing

    Errors are handled by returning None (and warning if ui is given), both
    in case of missing key:

    >>> tf = TextFiller('{some}/text/to/{fill}')
    >>> tf.fill(some='prefix', badfill='suffix')

    and of bad pattern:

    >>> tf = TextFiller('{some/text/to/{fill}')
    >>> tf.is_valid()
    False
    >>> tf.fill(some='prefix', fill='suffix')

    >>> tf = TextFiller('{some}/text/to/{fill:}')
    >>> tf.is_valid()
    False
    >>> tf.fill(some='prefix', fill='suffix')
    '''

    # Regexps used during parsing
    _re_pattern_lead = re.compile(r' ^ ([^{}]*) [{] (.*) $', re.VERBOSE)
    _re_pattern_cont = re.compile(r'''
    ^  ([a-zA-Z][a-zA-Z0-9_]*)          # name (leading _ disallowed on purpose)
       ((?: : [^{}:=]+ = [^{}:=]* )*)   # :sth=else  substitutions
       [}]
       (.*)                        $ ''', re.VERBOSE)
    _re_sub = re.compile(r'^ : ([^{}:=]+) = ([^{}:=]*)  (.*)  $', re.VERBOSE)

    def __init__(self, fill_text, ui=None):
        def percent_escape(val):
            """Escape %-s in given text by doubling them."""
            return val.replace('%', '%%')

        text = self.fill_text = fill_text
        # Replacement text. That's just percent 'some %(abc)s text' (we use % not '{}' to
        # leave chances of working on python 2.5). Empty value means I am broken
        self._replacement = None
        # List of substitutions, tuples:
        #   result synthetic name,
        #   base field name
        #   [(from, to), (from, to), ...]   list of substitutions to make
        self._substitutions = []

        replacement = ''
        synth_idx = 0
        while text:
            match = self._re_pattern_lead.search(text)
            if match:
                replacement += percent_escape(match.group(1))
                text = match.group(2)
                match = self._re_pattern_cont.search(text)
                if not match:
                    if ui:
                        ui.warn(_("Bad replacement pattern: %s") % fill_text)
                    return
                name, substs, text = match.group(1), match.group(2), match.group(3)
                if substs:
                    fixups = []
                    while substs:
                        match = self._re_sub.search(substs)
                        if not match:
                            if ui:
                                ui.warn(_("Bad replacement pattern: %s") % fill_text)
                            return
                        src, dest, substs = match.group(1), match.group(2), match.group(3)
                        fixups.append((src, dest))
                    synth_idx += 1
                    synth = "_" + str(synth_idx)
                    self._substitutions.append((synth, name, fixups))
                    name = synth
                replacement += '%(' + name + ')s'
            else:
                replacement += percent_escape(text)
                text = ''
        # Final save
        if ui:
            ui.debug(_("Replacement %s turned into expression %s") % (fill_text, replacement))
        self._replacement = replacement

    def is_valid(self):
        """Returns whether object is in correct state, or broken"""
        return bool(self._replacement)

    def fill(self, **kwargs):
        """Fills text with given arguments. If something is broken (missing key, broken pattern)
        returns None"""
        if not self._replacement:
            return None
        try:
            for made_field, src_field, fixups in self._substitutions:
                value = kwargs[src_field]
                for src, dest in fixups:
                    value = value.replace(src, dest)
                kwargs[made_field] = value
            return self._replacement % kwargs
        except:  # pylint:disable=bare-except
            return None

###########################################################################
# Config support
###########################################################################


def setconfig_dict(ui, section, items):
    """
    Set's many configuration items with one call. Defined mostly
    to make some code (including doctests below) a bit more readable.

    >>> import mercurial.ui; ui = mercurial.ui.ui()
    >>> setconfig_dict(ui, "sect1", {'a': 7, 'bbb': 'xxx', 'c': '-'})
    >>> setconfig_dict(ui, "sect2", {'v': 'vvv'})
    >>> ui.config("sect1", 'a')
    7
    >>> ui.config("sect2", 'v')
    'vvv'

    :param section: configuration section tofill
    :param items: dictionary of items to set
    """
    for key, value in items.iteritems():
        ui.setconfig(section, key, value)


def rgxp_config_items(ui, section, rgxp):
    r'''
    Yields items from given config section which match given regular
    expression.

    >>> import mercurial.ui; ui = mercurial.ui.ui()
    >>> setconfig_dict(ui, "foo", {
    ...         "pfx-some-sfx": "ala, ma kota",
    ...         "some.nonitem": "bela nie",
    ...         "x": "yes",
    ...         "pfx-other-sfx": 4})
    >>> setconfig_dict(ui, "notfoo", {
    ...         "pfx-some-sfx": "bad",
    ...         "pfx-also-sfx": "too",
    ...         })
    >>>
    >>> for name, value in rgxp_config_items(
    ...         ui, "foo", re.compile(r'^pfx-(\w+)-sfx$')):
    ...    print name, value
    some ala, ma kota
    other 4

    :param ui: mercurial ui, used to access config
    :param section: config section name
    :param rgxp: tested regexp, should contain single (group)

    :return: yields pairs (group-match, value) for all matching items
    '''
    for key, value in ui.configitems(section):
        match = rgxp.search(key)
        if match:
            yield match.group(1), value


def rgxp_configlist_items(ui, section, rgxp):
    r'''
    Similar to rgxp_config_items, but returned values are read using
    ui.configlist, so returned as lists.

    >>> import mercurial.ui; ui = mercurial.ui.ui()
    >>> setconfig_dict(ui, "foo", {
    ...         "pfx-some-sfx": "ala, ma kota",
    ...         "some.nonitem": "bela nie",
    ...         "x": "yes",
    ...         "pfx-other-sfx": "sth"})
    >>> setconfig_dict(ui, "notfoo", {
    ...         "pfx-some-sfx": "bad",
    ...         "pfx-also-sfx": "too",
    ...         })
    >>>
    >>> for name, value in rgxp_configlist_items(
    ...         ui, "foo", re.compile(r'^pfx-(\w+)-sfx$')):
    ...    print name, value
    some ['ala', 'ma', 'kota']
    other ['sth']

    :param ui: mercurial ui, used to access config
    :param section: config section name
    :param rgxp: tested regexp, should contain single (group)

    :return: yields pairs (group-match, value-as-list) for all
             matching items
    '''
    for key, _ in ui.configitems(section):
        match = rgxp.search(key)
        if match:
            yield match.group(1), ui.configlist(section, key)


def rgxp_configbool_items(ui, section, rgxp):
    r'''
    Similar to rgxp_config_items, but returned values are read using
    ui.configbool, so returned as lists.

    >>> import mercurial.ui; ui = mercurial.ui.ui()
    >>> setconfig_dict(ui, "foo", {
    ...         "pfx-some-sfx": "true",
    ...         "some.nonitem": "bela nie",
    ...         "x": "yes",
    ...         "pfx-other-sfx": "false"})
    >>> setconfig_dict(ui, "notfoo", {
    ...         "pfx-some-sfx": "1",
    ...         "pfx-also-sfx": "0",
    ...         })
    >>>
    >>> for name, value in rgxp_configbool_items(
    ...         ui, "foo", re.compile(r'^pfx-(\w+)-sfx$')):
    ...    print name, value
    some True
    other False

    :param ui: mercurial ui, used to access config
    :param section: config section name
    :param rgxp: tested regexp, should contain single (group)

    :return: yields pairs (group-match, value-as-list) for all
             matching items
    '''
    for key, _ in ui.configitems(section):
        match = rgxp.search(key)
        if match:
            yield match.group(1), ui.configbool(section, key)


def suffix_config_items(ui, section, suffix):
    """
    Yields items from given config section which match pattern '«sth».suffix'

    >>> import mercurial.ui; ui = mercurial.ui.ui()
    >>> setconfig_dict(ui, "foo", {
    ...         "some.item": "ala, ma kota",
    ...         "some.nonitem": "bela nie",
    ...         "x": "yes",
    ...         "other.item": 4})
    >>> setconfig_dict(ui, "notfoo", {
    ...         "some.item": "bad",
    ...         "also.item": "too",
    ...         })
    >>>
    >>> for name, value in suffix_config_items(
    ...         ui, "foo", 'item'):
    ...    print name, value
    some ala, ma kota
    other 4

    :param ui: mercurial ui, used to access config
    :param section: config section name
    :param suffix: expected suffix (without a dot)

    :return: yields pairs (prefix, value) for all matching items, values are lists
    """
    rgxp = re.compile(r'^(\w+)\.' + re.escape(suffix))
    for key, value in rgxp_config_items(ui, section, rgxp):
        yield key, value


def suffix_configlist_items(ui, section, suffix):
    """
    Similar to suffix_config_items, but returned values are read using
    ui.configlist, so returned as lists.

    >>> import mercurial.ui; ui = mercurial.ui.ui()
    >>> setconfig_dict(ui, "foo", {
    ...         "some.item": "ala, ma kota",
    ...         "some.nonitem": "bela nie",
    ...         "x": "yes",
    ...         "other.item": "kazimira"})
    >>> setconfig_dict(ui, "notfoo", {
    ...         "some.item": "bad",
    ...         "also.item": "too",
    ...         })
    >>>
    >>> for name, value in suffix_configlist_items(
    ...         ui, "foo", "item"):
    ...    print name, value
    some ['ala', 'ma', 'kota']
    other ['kazimira']

    :param ui: mercurial ui, used to access config
    :param section: config section name
    :param suffix: expected suffix (without a dot)

    :return: yields pairs (group-match, value-as-list) for all
             matching items, values are boolean
    """
    rgxp = re.compile(r'^(\w+)\.' + re.escape(suffix))
    for key, value in rgxp_configlist_items(ui, section, rgxp):
        yield key, value


def suffix_configbool_items(ui, section, suffix):
    """
    Similar to suffix_config_items, but returned values are read using
    ui.configbool, so returned as booleans.

    >>> import mercurial.ui; ui = mercurial.ui.ui()
    >>> setconfig_dict(ui, "foo", {
    ...         "true.item": "true",
    ...         "false.item": "false",
    ...         "one.item": "1",
    ...         "zero.item": "0",
    ...         "yes.item": "yes",
    ...         "no.item": "no",
    ...         "some.nonitem": "1",
    ...         "x": "yes"})
    >>> setconfig_dict(ui, "notfoo", {
    ...         "some.item": "0",
    ...         "also.item": "too",
    ...         })
    >>>
    >>> for name, value in suffix_configbool_items(
    ...         ui, "foo", "item"):
    ...    print name, str(value)
    zero False
    yes True
    one True
    true True
    no False
    false False
    >>>
    >>> ui.setconfig("foo", "text.item", "something")
    >>> for name, value in suffix_configbool_items(
    ...         ui, "foo", "item"):
    ...    print name, str(value)
    Traceback (most recent call last):
      File "/usr/lib/python2.7/dist-packages/mercurial/ui.py", line 237, in configbool
        % (section, name, v))
    ConfigError: foo.text.item is not a boolean ('something')

    :param ui: mercurial ui, used to access config
    :param section: config section name
    :param suffix: expected suffix (without a dot)

    :return: yields pairs (group-match, value) for all
             matching items
    """
    rgxp = re.compile(r'^(\w+)\.' + re.escape(suffix))
    for key, value in rgxp_configbool_items(ui, section, rgxp):
        yield key, value


###########################################################################
# Monkeypatching
###########################################################################

def monkeypatch_method(cls, fname=None):
    """
    Monkey-patches some method, replacing it with another
    implementation. Original method is preserved on ``.orig``
    attribute.

    >>> class SomeClass(object):
    ...    def meth(self, arg):
    ...        return "Original: " + arg
    >>>
    >>> @monkeypatch_method(SomeClass)
    ... def meth(self, arg):
    ...     return "Patched: " + meth.orig(self, arg)
    >>>
    >>> obj = SomeClass()
    >>> print obj.meth("some param")
    Patched: Original: some param

    It is also possible to use different name

    >>> class SomeClass(object):
    ...    def meth(self, arg):
    ...        return "Original: " + arg
    >>>
    >>> @monkeypatch_method(SomeClass, "meth")
    ... def another_meth(self, arg):
    ...     return "Patched: " + another_meth.orig(self, arg)
    >>>
    >>> obj = SomeClass()
    >>> print obj.meth("some param")
    Patched: Original: some param

    :param cls: Class being modified
    :param fname: Name of method being monkey-patched (if not given,
           name of decorated function is used)
    """
    def decorator(func):
        local_fname = fname
        if local_fname is None:
            local_fname = func.__name__
        setattr(func, "orig", getattr(cls, local_fname, None))
        setattr(cls, local_fname, func)
        return func
    return decorator


def monkeypatch_function(module, fname=None):
    """
    Monkey-patches some function, replacing it with another
    implementation. Original function is preserved on ``.orig``
    attribute.

    >>> import random
    >>> @monkeypatch_function(random)
    ... def seed(x=None):
    ...     print "Forcing random to seed with 0 instead of", x
    ...     return seed.orig(0)
    >>>
    >>> random.seed()
    Forcing random to seed with 0 instead of None
    >>> random.randint(0, 10)
    9

    >>> import random
    >>> @monkeypatch_function(random, 'choice')
    ... def choice_first(sequence):
    ...    return sequence[0]
    >>> for x in range(0, 4): print random.choice("abcdefgh")
    a
    a
    a
    a

    :param module: Module being modified
    :param fname: Name of function being monkey-patched (if not given,
           name of decorated function is used)
    """
    # In fact implementation is the same. But it is more readable
    # to use two names
    return monkeypatch_method(module, fname)


###########################################################################
# Locating repositories
###########################################################################

def find_repositories_below(path, check_inside=False):
    """Finds all Mercurial repositories in given directory tree.

    Works as generator, yielding full paths of all repositories found,
    ordered alphabetically.  If initial path is itself some
    repository, it is included.

    By default function does not look for embedded repositories (if we
    scan from ~/src and both ~/src/somerepo and ~/src/somerepo/subrepo
    are repositories, only the former will be yielded).  This can be
    changed by check_inside param

    :param path: Initial path
    :param check_inside: Shall we look for embedded repos?
    """
    # Impl. note: we do not use os.walk as it can be very costly
    # if some repo is big and deep.
    pending = deque([path])
    while pending:
        checked = pending.popleft()
        if os.path.isdir(os.path.join(checked, '.hg')):
            yield checked
            if not check_inside:
                continue
        names = os.listdir(checked)
        paths = [os.path.join(checked, name)
                 for name in names if name != '.hg']
        dir_paths = [path
                     for path in paths if os.path.isdir(path)]
        pending.extendleft(sorted(dir_paths, reverse=True))

