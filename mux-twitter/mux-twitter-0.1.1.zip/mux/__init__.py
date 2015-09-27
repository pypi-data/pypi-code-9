#!/usr/bin/env python
"""mux: cli twitter app using the streaming api
"""

import logging

__author__ = "Da_Blitz <code@blitz.works>"
__version__ = "0.1.1"
__email__ = "code@epic-man.com"
__license__ = "BSD (3 Clause)"
__url__ = "http://blitz.works"

EDITOR_ORDER = ["MUX_EDITOR", "VISUAL", "EDITOR"]
FALLBACK_EDITORS = ['sensible-editor']

TWITTER_MAX_LEN = 140

program_name = 'mux'
auth_file = "auth.ini"

log = logging.getLogger(program_name)
