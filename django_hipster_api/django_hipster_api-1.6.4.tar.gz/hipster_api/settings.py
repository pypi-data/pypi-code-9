# -*- coding: utf-8 -*-
import os
from django.conf import settings

DIR = os.path.join(os.path.dirname(__file__), 'templates')


def load_default():
    setattr(settings, 'TEMPLATE_DIRS',  getattr(settings, 'TEMPLATE_DIRS', ()) + (DIR, ))
