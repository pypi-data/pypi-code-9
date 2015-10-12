# -*- coding: utf-8 -*-
#
# path pattern: define global path aliases
#
# Copyright (c) 20015 Marcin Kasperski <Marcin.Kasperski@mekk.waw.pl>
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

"""Define your username per directory tree.

Use different name and/or email depending on where you work.  For
example, if you write in your ``~/.hgrc``::

    [extensions]
    dynamic_username =

    [dynamic_username]
    work.location = ~/work
    work.username = John Smith <john.smith@serious.com>
    hobby.location = ~/hobby, ~/blogging
    hobby.username = Johny <fastjohny@fantasy.net>

you will commit as John Smith in ``~/work/libs/payproc`` and as Johny
in ``~/blogging/travel``.

You can test effects by callling::

    hg showconfig ui.username

See extension README.txt or
http://bitbucket.org/Mekk/mercurial-dynamic_username/ for more info.
"""

from mercurial import commands, util
from mercurial.i18n import _

import re
import os

# pylint:disable=fixme,line-too-long,invalid-name
#   (invalid-name because of ui and cmdtable)

############################################################
# Utility classes and functions
############################################################

CONFIG_SECTION = "dynamic_username"


def lies_within_tree(child, parent):
    """
    Checks whether child lies anywhere inside parent tree. Child should be absolute path,
    parent will be tilda expanded and absolutized.

    :return: expanded canonicalized parent on match, None on mismatch
    """
    true_parent = os.path.abspath(os.path.expanduser(parent))
    pfx = os.path.commonprefix([child, true_parent])
    return pfx == true_parent and true_parent or None


def lookup_dynamic_username(ui, repo):
    """Checks whether any dynamic username is set for given repo. Returns it if so, returns None elsewhere"""
    # Looking up longest match
    if not hasattr(repo, 'root'):
        return None
    repo_path = os.path.abspath(repo.root)
    best_path = ''
    best_username = None
    re_location = re.compile("^(\w+)\.location$")
    for key, value in ui.configitems(CONFIG_SECTION):
        match = re_location.search(key)
        if match:
            prefix = match.group(1) + "."
            trees = ui.configlist(CONFIG_SECTION, prefix + "location")
            for tree in trees:
                canon_path = lies_within_tree(repo_path, tree)
                if canon_path:
                    if len(canon_path) > len(best_path):
                        best_path = canon_path
                        # This will also set best to None if we miss .username to revert to default
                        best_username = ui.config(CONFIG_SECTION, prefix + "username", None)

    return best_username

############################################################
# Mercurial extension hooks
############################################################

def reposetup(ui, repo):
    """Setup repo: rewrite ui/username if needed"""
    dynamic_name = lookup_dynamic_username(ui, repo)
    if dynamic_name:
        ui.debug(_("Updating username to dynamically-selected %s") % dynamic_name)
        ui.setconfig("ui", "username", dynamic_name)


############################################################
# Extension setup
############################################################

# testedwith = '3.0 3.1.2'
