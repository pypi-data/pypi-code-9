# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2012, 2013, 2014, 2015 CERN.
#
# Invenio is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""Journal field."""

from invenio.modules.deposit.field_base import WebDepositField

from wtforms import StringField

__all__ = ['JournalField']


class JournalField(WebDepositField, StringField):

    """Journal field (deprecated)."""

    def __init__(self, **kwargs):
        """Deprecated."""
        import warnings
        warnings.warn("Field has been deprecated", PendingDeprecationWarning)
        defaults = dict(
            icon='book',
            widget_classes="form-control",
        )
        defaults.update(kwargs)
        super(JournalField, self).__init__(**defaults)
