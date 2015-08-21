#----------------------------------------------------------------------------
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
#----------------------------------------------------------------------------
from __future__ import absolute_import

__all__ = ['__version__', 'setup']

try:  # pragma: no cover
    from trait_documenter._version import full_version as __version__
except ImportError:  # pragma: no cover
    __version__ = "not-built"


def setup(app):
    """ Add the TraitDocumenter in the current sphinx autodoc instance.

    """
    from trait_documenter.class_trait_documenter import ClassTraitDocumenter
    from trait_documenter.module_trait_documenter import ModuleTraitDocumenter

    app.add_autodocumenter(ModuleTraitDocumenter)
    app.add_autodocumenter(ClassTraitDocumenter)
