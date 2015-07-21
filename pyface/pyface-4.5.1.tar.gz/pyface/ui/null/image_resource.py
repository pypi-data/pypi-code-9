#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Enthought, Inc.
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------


# Standard library imports.
import os

# Enthought library imports.
from traits.api import Any, HasTraits, List, Property, provides
from traits.api import Unicode

# Local imports.
from pyface.i_image_resource import IImageResource, MImageResource


@provides(IImageResource)
class ImageResource(MImageResource, HasTraits):
    """ The 'null' toolkit specific implementation of an ImageResource.  See the
    IImageResource interface for the API documentation.
    """


    #### Private interface ####################################################

    # The resource manager reference for the image.
    _ref = Any

    #### 'ImageResource' interface ############################################

    absolute_path = Property(Unicode)

    name = Unicode

    search_path = List

    ###########################################################################
    # 'ImageResource' interface.
    ###########################################################################

    def create_bitmap(self, size=None):
        return self.create_image(size)

    def create_icon(self, size=None):
        return self.create_image(size)

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _get_absolute_path(self):
        # FIXME: This doesn't quite work with the new notion of image size. We
        # should find out who is actually using this trait, and for what!
        # (AboutDialog uses it to include the path name in some HTML.)
        ref = self._get_ref()
        if ref is not None:
            absolute_path = os.path.abspath(self._ref.filename)

        else:
            absolute_path = self._get_image_not_found().absolute_path

        return absolute_path

#### EOF ######################################################################
