# -*- coding: utf-8 -*-
#
# path pattern: define global path aliases, cloneto command
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

"""Define [paths] once and reuse over many repositories.

path_pattern
------------

This extension frees you from defining and maintaining [paths]
individually for every repository.  Instead, you may define general
patterns of how to resolve paths.

For example, write::

    [path_pattern]
    abc.local = ~/abcdevel/{repo}
    abc.remote =  ssh://johny@devel.abc.com/sources/{repo}
    dev.local = ~/sources/{repo}
    dev.remote =  https://tim@devel-department.local/{repo}

and use ``hg push abc`` in any repo kept below ``~/abcdevel`` or ``hg
pull dev`` in any repo below ``~/sources``.

cloneto
-------

The extension defines also ``cloneto`` helper, which clones current
repo to address specified by given path.  It works especially well
together with patterns.  With the example above:

    cd ~/sources/libs
    hg init xyz
    cd xyz
    hg cloneto dev

For more information, see path_pattern README or
http://bitbucket.org/Mekk/mercurial-path_pattern/
"""

from mercurial import commands, util
from mercurial.i18n import _

import mercurial_extension_utils as meu

import re

# pylint:disable=fixme,line-too-long,invalid-name
#   (invalid-name because of ui and cmdtable)

############################################################
# Utility classes and functions
############################################################


class PatternPair(object):
    """
    Represents individual path pattern - pair of local (like
    "~/sources/{path}") and remote (like "ssh://some/where/{path}")
    """
    def __init__(self, alias):
        self.alias = alias
        self.local = None
        self.remote = None
        self.enforce = False

    def lookup_remote(self, local_directory, ui):
        """
        Checks whether local directory matches, if so, returns
        matching remote, if not, returns None.
        """
        value = None
        if self.local and self.remote:
            match = self.local.search(local_directory)
            if match:
                value = self.remote.fill(**match)
                if not value:
                    ui.warn(_("Invalid path pattern - markers mismatch between %s.local and %s.remote\n")
                            % (self.alias, self.alias))
        return value

    def learn_local(self, path_text, ui):
        """Parse and save local path"""
        self.local = meu.DirectoryPattern(path_text, ui)

    def learn_remote(self, path_text, ui):
        """Parse and save remote path"""
        self.remote = meu.TextFiller(path_text, ui)
        # TODO: validate whether path_text looks like path

    def validate(self, ui):
        """Checks whether both sides are defined and valid. Warns about problems"""
        for name, obj in [("local", self.local),
                          ("remote", self.remote)]:
            if not obj:
                ui.warn(
                    _("Incomplete path pattern - missing %s.%s\n") % (self.alias, name))
                return False
            if not obj.is_valid():
                ui.warn(
                    _("Invalid path pattern %s.%s - bad syntax") % (self.alias, name))
                return False
        return True

    def describe(self):
        return _("%s%s\n    local:  %s\n    remote: %s") % (
            self.alias,
            self.enforce and "      [enforced over .hg/hgrc]" or "",
            self.local.pattern_text, self.remote.fill_text)


class PathPatterns(object):
    """
    Loads and parses pattern definitions
    """
    def __init__(self, ui):
        self.patterns = {}   # name → PatternPair
        # Read «sth».local
        for alias, value in meu.suffix_config_items(ui, "path_pattern", "local"):
            if alias not in self.patterns:
                self.patterns[alias] = PatternPair(alias)
            ui.debug(_("Parsing local side of path pattern %s") % alias)
            self.patterns[alias].learn_local(value, ui)
        # Read «sth».remote
        for alias, value in meu.suffix_config_items(ui, "path_pattern", "remote"):
            if alias not in self.patterns:
                self.patterns[alias] = PatternPair(alias)
            ui.debug(_("Parsing remote side of path pattern %s") % alias)
            self.patterns[alias].learn_remote(value, ui)
        # Read «sth».enforce
        for alias, value in meu.suffix_configbool_items(ui, "path_pattern", "enforce"):
            if alias in self.patterns:
                self.patterns[alias].enforce = value
        # Check for incomplete and invalid items
        for alias in self.patterns.keys()[:]:
            if not self.patterns[alias].validate(ui):
                del self.patterns[alias]

    def generate_paths(self, ui, repo):
        """
        Updates ui config with new path's for given repo, generated from patterns
        """
        # Reading known paths to avoid overwriting them
        known_paths = {}
        for key, value in ui.configitems("paths"):
            known_paths[key] = value
        # Actually applying new patterns
        for path_name, pattern_pair in self.patterns.iteritems():
            expanded = pattern_pair.lookup_remote(repo.root, ui)
            if expanded:
                if (not pattern_pair.enforce) and (path_name in known_paths):
                    ui.debug(_("Ignoring path pattern %s as repo %s has own path of this name\n") % (path_name, repo.root))
                else:
                    ui.debug(_("Defining path %s as %s\n") % (path_name, expanded))
                    ui.setconfig("paths", path_name, expanded)

    def print_patterns(self, ui, list_repos=False):
        """
        Prints pattern information to standard output
        """
        if self.patterns:
            ui.status(_("Defined path patterns:\n%s\n") % "\n".join(
                self.patterns[pname].describe()
                for pname in sorted(self.patterns.keys())))
        else:
            ui.status(_("No path patterns defined. Add [path_pattern] section to ~/.hgrc\n"))


############################################################
# Mercurial extension hooks
############################################################

patterns = None

# def uisetup(ui):
# Not used, better to load patterns later, config can be updated by plugins


def extsetup(ui):
    """Setup extension: load patterns definitions from config"""
    global patterns    # pylint:disable=global-statement
    patterns = PathPatterns(ui)


def reposetup(ui, repo):
    """Setup repo: add pattern-based paths to repository config"""
    # Checking whether this is local repository, for other types extension
    # is pointless. Unfortunately we can't test repo type, as some extensions
    # change it (for example hgext.git.hgrepo.hgrepo happens to me…)
    if not hasattr(repo, 'root'):
        return
    patterns.generate_paths(ui, repo)


############################################################
# Commands
############################################################


def cmd_list_path_patterns(ui, **opts):
    """
    List all active path patterns.
    """
    patterns.print_patterns(ui)


def cmd_cloneto(ui, repo, path_alias, **opts):
    """
    Clone current repository to (usually remote) url
    pointed by already defined path alias::

        hg cloneto somealias

    is equivalent to::

        hg clone . <aliaspath>

    where <aliaspath> is whatever somealias expands to
    according to ``hg paths``.

    Command most useful together with path_pattern. 
    """
    known_paths = []
    for key, value in ui.configitems("paths"):
        if key == path_alias:
            ui.status(_("Cloning current repository to %s (resolved from: %s)\n" % (value, path_alias)))
            return commands.clone(ui, source=repo, dest=value)
        else:
            known_paths.append(key)
    # Failing helpfully
    if known_paths:
        raise util.Abort(_("Unknown alias: %s. Defined path aliases: %s") % (
            path_alias, ", ".join(known_paths)))
    else:
        raise util.Abort(_("Uknown alias: %s. No paths defined, consider creating some paths or path_patterns") % path_alias)

############################################################
# Extension setup
############################################################

# testedwith = '3.0 3.1.2'
commands.norepo += " list_path_patterns"
cmdtable = {
    "list_path_patterns": (
        cmd_list_path_patterns,
        [
            # ('r', 'list-repos', None, 'List repositories matching the pattern'),
        ],
        "hg list_path_patterns"),
    "cloneto": (
        cmd_cloneto,
        [],
        "hg cloneto ALIAS"),
}
