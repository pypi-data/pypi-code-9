# -*- coding: utf-8 -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2015 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU Affero General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option)
#  any later version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for
#  more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Database Utilities
"""

from __future__ import unicode_literals

# TODO: Deprecate/remove these imports.
from alembic.util import obfuscate_url_pw
from rattail.db.config import engine_from_config, get_engines, get_default_engine, configure_session


def maxlen(attr):
    """
    Return the maximum length for the given attribute.
    """
    if len(attr.property.columns) == 1:
        type_ = attr.property.columns[0].type
        return getattr(type_, 'length', None)
