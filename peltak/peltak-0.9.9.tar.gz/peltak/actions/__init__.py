# -*- coding: utf-8 -*-
"""
Action manager.


**registering actions**


**Example action**

.. code-block:: python

    from peltak.actions import actions
    from peltak.core import git

    @actions.register('action-name')
    def myaction(app):
        print("Current branch: {}".format(git.current_branch()))
"""
from igor.plugins import SimplePluginManager
from ..config import ACTIONS_DIRS
actions = SimplePluginManager(ACTIONS_DIRS)
