# -*- coding: utf-8 -*-
from trytond.pool import Pool
from .async import Async, task    # noqa


def register():
    Pool.register(
        Async,
        module='async', type_='model'
    )
