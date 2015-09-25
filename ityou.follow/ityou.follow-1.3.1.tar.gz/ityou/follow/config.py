# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------
Configuration of the ityou.follow module
--------------------------------------------------------------------------------
"""

# --- qsql Database Table --------
TABLE_FOLLOWS = 'follows'
TABLE_LIKES = 'likes'

# LIKE/DISLIKE should not be displayed in the following views
TEMPLATE_BLACKLIST = [
    'solgemafullcalendar_view',
]



