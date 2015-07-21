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
""" The base class for all actions. """


# Enthought library imports.
from traits.api import Bool, Callable, Enum, HasTraits, Instance, Str
from traits.api import Unicode
from traitsui.ui_traits import Image


class Action(HasTraits):
    """ The base class for all actions.

    An action is the non-UI side of a command which can be triggered by the end
    user.  Actions are typically associated with buttons, menu items and tool
    bar tools.

    When the user triggers the command via the UI, the action's 'perform'
    method is invoked to do the actual work.

    """

    #### 'Action' interface ###################################################

    # Keyboard accelerator (by default the action has NO accelerator).
    accelerator = Unicode

    # Is the action checked?  This is only relevant if the action style is
    # 'radio' or 'toggle'.
    checked = Bool(False)

    # A longer description of the action (used for context sensitive help etc).
    # If no description is specified, the tooltip is used instead (and if there
    # is no tooltip, then well, maybe you just hate your users ;^).
    description = Unicode

    # Is the action enabled?
    enabled = Bool(True)

    # Is the action visible?
    visible = Bool(True)

    # The action's unique identifier (may be None).
    id = Str

    # The action's image (displayed on tool bar tools etc).
    image = Image

    # The action's name (displayed on menus/tool bar tools etc).
    name = Unicode

    # An (optional) callable that will be invoked when the action is performed.
    on_perform = Callable

    # The action's style.
    style = Enum('push', 'radio', 'toggle')

    # A short description of the action used for tooltip text etc.
    tooltip = Unicode

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    #### Initializers #########################################################

    def _id_default(self):
        """ Initializes the 'id' trait. """

        return self.name

    #### Methods ##############################################################

    def destroy(self):
        """ Called when the action is no longer required.

        By default this method does nothing, but this would be a great place to
        unhook trait listeners etc.

        """

        return

    def perform(self, event):
        """ Performs the action. """

        if self.on_perform is not None:
            self.on_perform()

        return

#### EOF ######################################################################
