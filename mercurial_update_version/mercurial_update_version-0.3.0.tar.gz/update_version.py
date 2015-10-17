# -*- coding: utf-8 -*-
#
# update_version: automatically fix version numbers while tagging
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

"""Let 'hg tag' automatically update version numbers in your code.

Manually maintaining various VERSION variables is both painful and
mistake-prone.  This extension automatically updates those values
whenever you tag a new release.

For example, write in your repository ``.hg/hgrc``::

    [update_version]
    active = true
    language = python
    tagfmt = dotted

and whenever you type::

    hg tag 0.3.7

files like setup.py, __init__.py, and version.py will be scanned for
version variables, and those will be updated to contain ``0.3.7``.

There are more usage options (enabling for many repositories
selected by location, configuring which files are scanned and
which expressions are updated). See extension README.txt or
http://bitbucket.org/Mekk/mercurial-update_version/
"""

from mercurial import commands, util
from mercurial.i18n import _

import re
import os

import mercurial_extension_utils as meu

# pylint:disable=fixme,line-too-long,invalid-name
#   (invalid-name because of ui and cmdtable)

############################################################
# Interfaces / base classes
############################################################


class Language(object):
    """Represents language rules"""

    # Files bigger than this limit should not be edited
    SIZE_LIMIT = 16384

    def format_version_no(self, version_parts):
        """
        To be overridden. Formats version string to be used in code.

        :param version_parts: tuple like ("1", "2") or ("1", "7", "04")
                - version number extracted from tag
        :return: formatted string appropriate for language or None
                 if given version is invalid for it (too short, to long etc)
        """
        raise util.Abort(_("Not implemented"))

    def worth_checking(self, filename, repo_root):
        """
        To be overridden. Checks whether given file should be
        checked (matches name pattern, depth in repo etc).
        Called by default locate_files, not used if locate_files
        is overridden.

        :param filename: File name (full path)
        :param repo_root: Repository root (full path)
        :return: True if file should be considered, False if not
        """
        raise util.Abort(_("Not implemented"))

    def locate_files(self, ui, repo):
        """Yields all files, which should be checked.

        Can be overridden, by default iterates over all repository
        files (as returned by manifest) and filters them by worth_checking
        and by size limit.
        """
        for fname in self.manifest(repo):
            if self.worth_checking(fname, repo.root):
                size = os.path.getsize(fname)
                if size <= self.SIZE_LIMIT:
                    yield fname
                else:
                    ui.debug(_("Ignoring big file %s (%d bytes)\n") % (fname, size))

    def update_line(self, line, version, basename):
        """Edits single line.

        To be overridden. Called by default update_file.

        :param line: complete input line, without final newline
        :param version: version number to save, whatever
               format_version_no returned
        :param basename: checked file basename (to be used in case
               a few file variants can be handled)
        :return: updated line or None if no changes were needed
               (return updated line if it already contains proper
               version number). Returned value should not have final newline
        """
        raise util.Abort(_("Not implemented"))

    def update_file(self, ui, filename, version, dry_run=False):
        """Edits given file, fixing version to given number

        Can be overridden. By default iterates over file lines
        and calls update_line

        :param filename: file to edit, full path
        :param version: version number, whatever format_version_no returned
        :param dry_run: does not save
        :return: list of triples (lineno, before, after)
        """
        file_lines = []
        changes = []
        basename = os.path.basename(filename)

        with open(filename, "r") as input:
            line_no = 0
            for line in input:
                line_no += 1
                stripped_line = line.rstrip("\r\n")
                fixed_line = self.update_line(line, version, basename)
                if fixed_line is None:
                    file_lines.append(line)
                else:
                    # Reintroduce final newline
                    fixed_line += line[len(stripped_line):]
                    file_lines.append(fixed_line)
                    if fixed_line != line:
                        changes.append((line_no, line, fixed_line))
                    else:
                        ui.status(_("Line %d in %s already contains proper version number") % (line_no, basename))

        if changes:
            if not dry_run:
                with open(filename, "w") as output:
                    output.writelines(file_lines)
        return changes

    def manifest(self, repo):
        """Helper. Yields all repository files"""
        ctx = repo['.']
        for fname in ctx.manifest():
            yield fname


class TagFmt(object):
    """Represents tag numbering format"""

    sample = ""

    def extract_no(self, tag_text):
        """Returns tag number or None if tag does not match pattern

        :param tag_text: whatever used gave
        :return: tag number as string tuple like ("1","0","2") or ("3","08") or None
        """
        raise util.Abort(_("Not implemented"))


############################################################
# Languages
############################################################

known_languages = {}


class LanguagePython(Language):
    tested_file_names = ['setup.py', 'version.py', '__init__.py']

    def format_version_no(self, version_parts):
        return ".".join(str(vp) for vp in version_parts)

    def worth_checking(self, filename, repo_root):
        return os.path.basename(filename) in self.tested_file_names

    def update_line(self, line, version, basename):
        match = self.re_version_line.search(line)
        if match:
            return match.group('before') + version + match.group('after')
        else:
            return None

    re_version_line = re.compile(r'''
    ^   (?P<before>
             \s* VERSION \s* = \s*
             (?P<quote> ["'] )      )
        (?P<version> \d+(?:\.\d+)+  )
        (?P<after>
             (?P=quote)   # closing quote
             .* )
    $ ''', re.VERBOSE)

known_languages['python'] = LanguagePython()


class LanguagePerl(Language):

    def format_version_no(self, version_parts):
        if len(version_parts) == 2:
            return ".".join(version_parts)
        if len(version_parts) == 3:
            txt = version_parts[0] + "."
            for item in version_parts[1:]:
                if len(item) > 2:
                    return None
                txt += "0" * (2 - len(item)) + item
            return txt
        return None

    def worth_checking(self, filename, repo_root):
        return filename.endswith(".pm") \
            or filename.endswith(".pl") \
            or filename.endswith(".pod") \
            or os.path.basename(filename) == "dist.ini"

    def update_line(self, line, version, basename):
        if basename.endswith(".ini"):
            rgxps = self.re_ini_rgxps
        else:
            rgxps = self.re_perl_rgxps
        for rgxp in rgxps:
            match = rgxp.search(line)
            if match:
                return match.group('before') + version + match.group('after')
        return None

    re_ini_rgxps = [
        re.compile('''
        ^   (?P<before>
                 \s* version \s* = \s*  )
        (?P<version> \d+(?:\.\d+)+  )
        (?P<after>
             \s*  (?:\#.*)?  )
        $ ''', re.VERBOSE),
    ]

    re_perl_rgxps = [
        re.compile(r'''
        ^  (?P<before>
               \s* (?: my | our | ) \s*
               \$ VERSION \s* = \s*
               (?P<quote> ["'] )         )
           (?P<version> \d+\.\d+         )
           (?P<after> 
               (?P=quote)   # closing quote
               .* )
        $ ''', re.VERBOSE),
        re.compile(r'''
        ^  (?P<before>
               \s* use \s+ constant \s+ VERSION \s* => \s* 
               (?P<quote> ["'] )         )
           (?P<version> \d+\.\d+         )
           (?P<after> 
               (?P=quote)   # closing quote
               .* )
        $ ''', re.VERBOSE),
        re.compile(r'''
        ^  (?P<before> \s* Version \s+ )
           (?P<ver> \d+\.\d+           )
           (?P<after> \s*              )
           $
        ''', re.VERBOSE),
    ]

known_languages['perl'] = LanguagePerl()


############################################################
# Tag formats
############################################################

known_tagfmts = {}


class TagFmtDotted(TagFmt):
    sample = "1.3.11"
    _re_tag = re.compile(r'^ ( \d+ (?:\.\d+)+ )$', re.VERBOSE)
    def extract_no(self, tag_text):
        match = self._re_tag.search(tag_text)
        if match:
            return match.group(1).split(".")
        else:
            return None

known_tagfmts['dotted'] = TagFmtDotted()


class TagFmtDashed(TagFmt):
    sample = "1-3-11"
    _re_tag = re.compile(r'^ ( \d+ (?:-\d+)+ )$', re.VERBOSE)
    def extract_no(self, tag_text):
        match = self._re_tag.search(tag_text)
        if match:
            return match.group(1).split("-")
        else:
            return None

known_tagfmts['dashed'] = TagFmtDashed()


class TagFmtPfxDotted(TagFmt):
    sample = "mylib-1.3.11"
    _re_tag = re.compile(r'^ .* - ( \d+ (?:\.\d+)+ )$', re.VERBOSE)
    def extract_no(self, tag_text):
        match = self._re_tag.search(tag_text)
        if match:
            return match.group(1).split(".")
        else:
            return None

known_tagfmts['pfx-dotted'] = TagFmtPfxDotted()


class TagFmtPfxDashed(TagFmt):
    sample = "mylib_1-3-11"
    _re_tag = re.compile(r'^ .*[^\d] [-_] ( \d+ (?:\-\d+)+ )$', re.VERBOSE)
    def extract_no(self, tag_text):
        match = self._re_tag.search(tag_text)
        if match:
            return match.group(1).split("-")
        else:
            return None

known_tagfmts['pfx-dashed'] = TagFmtPfxDashed()


############################################################
# Actual extension work
############################################################


def is_active_on(ui, repo):
    """Checks whether extension is to be active on given repo.
    Returns pair of (language, tagfmt) names if so, None, None if not."""

    def read_details(ui, language_tag, tagfmt_tag):
        language = ui.config("update_version", language_tag, None)
        if not language:
            ui.warn(_("%s not set in [update_version] section") % language_tag)
            return None, None
        tagfmt = ui.config("update_version", tagfmt_tag, None)
        if not tagfmt:
            ui.warn(_("%s not set in [update_version] section") % tagfmt_tag)
            return None, None
        return language, tagfmt

    if not hasattr(repo, 'root'):
        return None, None
    # enabled by active
    if ui.configbool("update_version", "active", False):
        ui.debug(_("update_version: active on %s due to active=true\n") % (repo.root))
        return read_details(ui, "language", "tagfmt")
    # enabled by active_on
    active_on = ui.configlist("update_version", "active_on", [])
    if active_on:
        if meu.belongs_to_tree_group(repo.root, active_on):
            ui.debug(_("update_version: active on %s due to active_on=%s\n") % (repo.root, ", ".join(active_on)))
            return read_details(ui, "language", "tagfmt")
        else:
            ui.debug(_("update_version: mismatch, %s does not match active_on=%s\n") % (repo.root, ", ".join(active_on)))
    # enabled by label.active_on
    for name, items in meu.suffix_configlist_items(
            ui, "update_version", "active_on"):
        if meu.belongs_to_tree_group(repo.root, items):
            ui.debug(_("update_version: active on %s due to %s.active_on=%s\n") % (repo.root, name, ", ".join(items)))
            return read_details(ui, name + ".language", name + ".tagfmt")
        else:
            ui.debug(_("update_version: mismatch, %s does not match %s.active_on=%s\n") % (repo.root, name, ", ".join(items)))
    return None, None


def update_repository(ui, repo, tag_name, dry_run=False):
    """Perform main actual action"""

    language_name, tagfmt_name = is_active_on(ui, repo)
    if not language_name:
        return

    language = known_languages.get(language_name)
    if not language:
        ui.warn(_("update_version: Unknown language %s") % language)
        return
    tagfmt = known_tagfmts.get(tagfmt_name)
    if not tagfmt:
        ui.warn(_("update_version: Unknown tagfmt %s") % tagfmt)
        return

    version = tagfmt.extract_no(tag_name)
    if not version:
        ui.warn(_("update_version: Invalid tag format: %s (expected %s, for example %s)") % (
            tag_name, tagfmt_name, tagfmt.sample))
        return False  # means OK

    fmt_version = language.format_version_no(version)
    if not fmt_version:
        ui.warn(_("update_version: Version number not supported by %s language: %s (too many parts or number too big)") % (
            language_name, ".".join(version)))
        return True  # means FAIL

    # Apply version number on files
    changed_files = []
    for fname in language.locate_files(ui, repo):
        changes = language.update_file(ui, fname, fmt_version, dry_run)
        if changes:
            ui.status(_("update_version: Version number in %s set to %s. List of changes:\n") % (fname, fmt_version))
            for lineno, before, after in changes:
                ui.status(_("    Line %d\n    < %s\n    > %s\n") % (
                    lineno, before.rstrip("\r\n"), after.rstrip("\r\n")))
            changed_files.append(fname)

    # Commit those changes
    if (not dry_run) and changed_files:
        ui.note("update_version: Commiting updated version number\n")
        commands.commit(
            ui, repo,
            *changed_files,
            message=_("Version number set to %s") % fmt_version)


############################################################
# Mercurial extension hooks
############################################################

# Note: as we commit something (updated numbers), the whole action
# must work as pre-tag hook, not pretag! During pretag the changeset
# being tagged is already set (and tag would omit the number-updating
# commit).
#
# According to mercurial docs, pre- hooks should be set during uisetup
# phase, so we enable them during uisetup below…

def pre_tag_hook(ui, repo, hooktype, pats, opts, **kwargs):
    """Hook called before tagging"""

    # Check command arguments. Ignore local tags, tags removal,
    # tags placed by revision (hg tag -r ... sth), unhandled arguments.
    # Extract final tag value.
    if opts.get('local'):
        ui.note("update_version: ignoring local tag\n")
        return
    if opts.get('remove'):
        ui.note("update_version: ignoring tag removal\n")
        return
    if opts.get('rev'):
        ui.note("update_version: ignoring tag placed by rev\n")
        return
    if len(pats) != 1:
        ui.warn("update_version: unexpected arguments, pats=%s\n" % pats)
        return True  # means fail

    tag_name = pats[0]
    update_repository(ui, repo, tag_name)

    return False #means ok


def uisetup(ui):
    """Enable pre-tag hook"""
    ui.setconfig("hooks", "pre-tag.update_version", pre_tag_hook)


############################################################
# Commands
############################################################

def cmd_tag_version_test(ui, repo, tag, **opts):
    """
    Dry-run, listing what would be changed
    """
    language_name, tagfmt_name = is_active_on(ui, repo)
    if not language_name:
        ui.status(_("update_version: not active in this repository\n"))
        return
    ui.status(_("update_version: using %s language rules and %s tag format\n")
              % (language_name, tagfmt_name))

    update_repository(ui, repo, tag, dry_run=True)


############################################################
# Extension setup
############################################################

# testedwith = '3.0 3.1.2'
cmdtable = {
    "tag_version_test": (
        cmd_tag_version_test,
        [
            # no arguments
        ],
        "hg tag_version_test TAG")
}
