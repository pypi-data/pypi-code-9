# ---------------------------------------------------------------------------
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in /LICENSE.txt and may be redistributed only
#  under the conditions described in the aforementioned license.  The license
#  is also available online at http://www.enthought.com/licenses/BSD.txt
#
#  Thanks for using Enthought open source!
#
# ---------------------------------------------------------------------------
from __future__ import unicode_literals

import sys
import traceback

from sphinx.ext.autodoc import ClassLevelDocumenter
from traits.has_traits import MetaHasTraits

from .util import get_trait_definition, DefinitionError


class ClassTraitDocumenter(ClassLevelDocumenter):
    """ Specialised Documenter subclass for class trait attributes.

    The class defines a new documenter that recovers the trait definition
    signature of class level traits.

    """

    objtype = 'traitattribute'
    directivetype = 'attribute'
    member_order = 60

    # must be higher than other attribute documenters
    priority = 12

    @classmethod
    def can_document_member(cls, member, membername, isattr, parent):
        """ Check that the documented member is a trait instance.
        """
        obj = parent.object
        return (
            isattr and
            isinstance(obj, MetaHasTraits) and
            membername in obj.__class_traits__)

    def document_members(self, all_members=False):
        """ Trait attributes have no members """

    def add_content(self, more_content, no_docstring=False):
        # Never try to get a docstring from the trait object.
        ClassLevelDocumenter.add_content(
            self, more_content, no_docstring=True)

    def import_object(self):
        """ Setup the necessary info for documenting the trait definition.

        Notes
        -----
        Code adapted from autodoc.Documenter.import_object.

        """
        dbg = self.env.app.debug
        if self.objpath:
            dbg('[autodoc] from %s import %s',
                self.modname, '.'.join(self.objpath))
        try:
            dbg('[autodoc] import %s', self.modname)
            __import__(self.modname)
            parent = self.module = sys.modules[self.modname]
            for part in self.objpath[:-1]:
                dbg('[autodoc] getattr(_, %r)', part)
                parent = self.get_attr(parent, part)
                dbg('[autodoc] => %r', parent)
            name = self.objpath[-1]
            self.object_name = name
            self.object = None  # We do have a trait object
            self.parent = parent
            return True
        # this used to only catch SyntaxError, ImportError and AttributeError,
        # but importing modules with side effects can raise all kinds of errors
        except (Exception, SystemExit) as e:
            if self.objpath:
                errmsg = 'autodoc: failed to import %s %r from module %r' % \
                         (self.objtype, '.'.join(self.objpath), self.modname)
            else:
                errmsg = 'autodoc: failed to import %s %r' % \
                         (self.objtype, self.fullname)
            if isinstance(e, SystemExit):
                errmsg += ('; the module executes module level statement ' +
                           'and it might call sys.exit().')
            else:
                errmsg += '; the following exception was raised:\n%s' % \
                          traceback.format_exc()
            dbg(errmsg)
            self.directive.warn(errmsg)
            self.env.note_reread()
            return False

    def add_directive_header(self, sig):
        """ Add the sphinx directives.

        Add the 'attribute' directive with the annotation option
        set to the trait definition.

        """
        ClassLevelDocumenter.add_directive_header(self, sig)
        if hasattr(self, 'get_sourcename'):
            sourcename = self.get_sourcename()
        else:
            sourcename = u'<autodoc>'
        try:
            definition = get_trait_definition(self.parent, self.object_name)
        except DefinitionError as error:
            self.directive.warn(error.args[0])
        else:
            self.add_line(
                '   :annotation: = {0}'.format(definition), sourcename)
