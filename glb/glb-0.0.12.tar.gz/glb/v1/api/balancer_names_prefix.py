# -*- coding: utf-8 -*-

from . import Resource
from glb.core.extensions import db


class BalancerNamesPrefix(Resource):

    def get(self, prefix):
        prefixed_names = db.get_prefixed_balancer_names(prefix)
        return prefixed_names, 200, None
