# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from glb.core.util import CRUDMixin


class Model(CRUDMixin, object):
    __abstract__ = True
