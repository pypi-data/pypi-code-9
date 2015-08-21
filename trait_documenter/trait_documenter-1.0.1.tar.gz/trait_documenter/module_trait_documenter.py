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

from sphinx.ext.autodoc import (
    ModuleLevelDocumenter, ModuleDocumenter, annotation_option, SUPPRESS)

from .util import get_trait_definition, DefinitionError


class ModuleTraitDocumenter(ModuleLevelDocumenter):
    """ Specialised Documenter subclass for module level traits.

    The class defines a new documenter that recovers the trait definition
    signature of class level traits.

    """
    objtype = 'data'
    member_order = 40
    option_spec = dict(ModuleLevelDocumenter.option_spec)
    option_spec["annotation"] = annotation_option

    # must be higher than other data documenters
    priority = -5

    @classmethod
    def can_document_member(cls, member, membername, isattr, parent):
        """ Check that the documented member is a trait instance.
        """
        return (
            isattr and
            hasattr(member, 'as_ctrait') and
            isinstance(parent, ModuleDocumenter))

    def document_members(self, all_members=False):
        """ Trait attributes have no members """

    def add_content(self, more_content, no_docstring=False):
        # Never try to get a docstring from the trait object.
        ModuleLevelDocumenter.add_content(self, more_content, no_docstring=True)

    def add_directive_header(self, sig):
        """ Add the sphinx directives.

        Add the 'attribute' directive with the annotation option
        set to the trait definition.

        """
        ModuleLevelDocumenter.add_directive_header(self, sig)
        if hasattr(self, 'get_sourcename'):
            sourcename = self.get_sourcename()
        else:
            sourcename = '<autodoc>'
        if not self.options.annotation:
            try:
                definition = get_trait_definition(
                    self.parent, self.object_name)
            except DefinitionError as error:
                self.directive.warn(error.args[0])
                return

            self.add_line(
                '   :annotation: = {0}'.format(definition), sourcename)
        elif self.options.annotation is SUPPRESS:
            pass
        else:
            self.add_line(
                '   :annotation: %s' % self.options.annotation, sourcename)
