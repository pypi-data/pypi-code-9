# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings


SHOP_ID = getattr(settings, 'SHOP_WSPAY_SHOP_ID', '')
SECRET_KEY = getattr(settings, 'SHOP_WSPAY_SECRET_KEY', '')
FORM_URL = getattr(settings, 'SHOP_WSPAY_FORM_URL', '')
