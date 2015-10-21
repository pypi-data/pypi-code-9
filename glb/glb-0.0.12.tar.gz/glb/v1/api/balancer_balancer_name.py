# -*- coding: utf-8 -*-
from . import Resource
from glb.core.extensions import db
from glb.core.errors import notfounderror


class BalancerBalancerName(Resource):

    def get(self, balancer_name):
        balancer = db.get_balancer(balancer_name)
        if balancer:
            return balancer, 200, None
        else:
            return notfounderror()

    def delete(self, balancer_name):
        res = db.delete_balancer(balancer_name)
        if res:
            db.update_service_latest_version('haproxy')
        return res, 200, None
