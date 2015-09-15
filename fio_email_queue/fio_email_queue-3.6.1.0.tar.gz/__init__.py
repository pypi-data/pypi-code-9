# -*- coding: utf-8 -*-
"""
    __init__.py

"""
from trytond.pool import Pool

from email_queue import EmailQueue


def register():
    Pool.register(
        EmailQueue,
        module='email_queue', type_='model'
    )
