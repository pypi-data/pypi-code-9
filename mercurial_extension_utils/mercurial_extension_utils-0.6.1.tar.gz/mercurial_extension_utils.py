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

from mercurial import commands, util
from mercurial.i18n import _

import re
import os

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


def rgxp_config_items(ui, section, rgxp):
    """
    Yields items from given config section which match given regular
    expression.

    >>> from mercurial import ui; u = ui.ui()
    >>> u.setconfig("foo", "some.item", 1)
    >>> u.setconfig("foo", "some.nonitem", 1)
    >>> u.setconfig("foo", "x", "yes")
    >>> u.setconfig("foo", "other.item", 4)
    >>> u.setconfig("notfoo", "other.item", "x")
    >>> for name, value in rgxp_config_items(
    ...         u, "foo", re.compile(r'^(\w+)\.item$')):
    ...    print name, value
    some 1
    other 4

    :param ui: mercurial ui, used to access config
    :param section: config section name
    :param rgxp: tested regexp, should contain single (group)

    :return: yields pairs (group-match, value) for all matching items
    """
    for key, value in ui.configitems(section):
        match = rgxp.search(key)
        if match:
            yield match.group(1), value


def rgxp_configlist_items(ui, section, rgxp):
    """
    Similar to rgxp_config_items, but returned values are read using
    ui.configlist, so returned as lists.

    >>> from mercurial import ui; u = ui.ui()
    >>> u.setconfig("foo", "some.item", "ala, ma, kota")
    >>> u.setconfig("foo", "some.nonitem", "bela nie")
    >>> u.setconfig("foo", "x", "yes")
    >>> u.setconfig("foo", "other.item", "kazimira")
    >>> u.setconfig("notfoo", "other.item", "x")
    >>> for name, value in rgxp_configlist_items(
    ...         u, "foo", re.compile(r'^(\w+)\.item$')):
    ...    print name, value
    some ['ala', 'ma', 'kota']
    other ['kazimira']

    :param ui: mercurial ui, used to access config
    :param section: config section name
    :param rgxp: tested regexp, should contain single (group)

    :return: yields pairs (group-match, value-as-list) for all
             matching items
    """
    for key, value in ui.configitems(section):
        match = rgxp.search(key)
        if match:
            yield match.group(1), ui.configlist(section, key)

def suffix_config_items(ui, section, suffix):
    """
    Yields items from given config section which match pattern '«sth».suffix'

    >>> from mercurial import ui; u = ui.ui()
    >>> u.setconfig("foo", "some.item", 1)
    >>> u.setconfig("foo", "some.nonitem", 1)
    >>> u.setconfig("foo", "x", "yes")
    >>> u.setconfig("foo", "other.item", 4)
    >>> u.setconfig("notfoo", "other.item", "x")
    >>> for name, value in suffix_config_items(
    ...         u, "foo", 'item'):
    ...    print name, value
    some 1
    other 4

    :param ui: mercurial ui, used to access config
    :param section: config section name
    :param suffix:

    :return: yields pairs (prefix, value) for all matching items
    """
    rgxp = re.compile(r'^(\w+)\.' + re.escape(suffix))
    for key, value in rgxp_config_items(ui, section, rgxp):
        yield key, value


def suffix_configlist_items(ui, section, suffix):
    """
    Similar to suffix_config_items, but returned values are read using
    ui.configlist, so returned as lists.

    >>> from mercurial import ui; u = ui.ui()
    >>> u.setconfig("foo", "some.item", "ala, ma, kota")
    >>> u.setconfig("foo", "some.nonitem", "bela nie")
    >>> u.setconfig("foo", "x", "yes")
    >>> u.setconfig("foo", "other.item", "kazimira")
    >>> u.setconfig("notfoo", "other.item", "x")
    >>> for name, value in suffix_configlist_items(
    ...         u, "foo", "item"):
    ...    print name, value
    some ['ala', 'ma', 'kota']
    other ['kazimira']

    :param ui: mercurial ui, used to access config
    :param section: config section name
    :param rgxp: tested regexp, should contain single (group)

    :return: yields pairs (group-match, value-as-list) for all
             matching items
    """
    rgxp = re.compile(r'^(\w+)\.' + re.escape(suffix))
    for key, value in rgxp_configlist_items(ui, section, rgxp):
        yield key, value

