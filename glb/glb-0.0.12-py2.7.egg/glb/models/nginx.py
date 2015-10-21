# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .base import Model


class Nginx(Model):

    __prefix_key__ = 'nginx'


class Upstream(Model):
    __prefix_key__ = 'upstreams'


class Server(Model):
    __prefix_key__ = 'servers'

