# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2013, 2014, 2015 CERN.
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

"""Deprecated."""

from invenio.modules.deposit.field_base import WebDepositField

from wtforms import StringField

from ..processor_utils import record_id_process

__all__ = ['RecordIDField']


class RecordIDField(WebDepositField, StringField):

    """Used to update existing records."""

    def __init__(self, **kwargs):
        """Deprecated."""
        import warnings
        warnings.warn("Field has been deprecated", PendingDeprecationWarning)
        defaults = dict(
            icon='barcode',
            export_key='recid',
            processors=[record_id_process],
            widget_classes="form-control"
        )
        defaults.update(kwargs)
        super(RecordIDField, self).__init__(**defaults)
