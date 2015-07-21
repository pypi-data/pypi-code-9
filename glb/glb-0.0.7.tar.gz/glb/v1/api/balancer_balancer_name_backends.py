# -*- coding: utf-8 -*-
from flask import g

from . import Resource
from glb.models.backend import Backend as BackendModel
from glb.core.extensions import db
from glb.core.errors import notfounderror


class BalancerBalancerNameBackends(Resource):

    def get(self, balancer_name):
        backends = db.get_backend_list(balancer_name)
        return backends, 200, None

    def post(self, balancer_name):
        balancer = db.get_balancer(balancer_name)
        if balancer:
            for backend in g.json:
                b = BackendModel(**backend)
                db.save_backend(b, balancer_name)
            return True, 201, None
        else:
            return notfounderror()

    def put(self, balancer_name):
        balancer = db.get_balancer(balancer_name)
        if balancer:
            for backend in g.json:
                b = BackendModel(**backend)
                db.save_backend(b, balancer_name)
            return True, 200, None
        else:
            return notfounderror

    def delete(self, balancer_name):
        res = db.delete_backend(balancer_name)
        if res:
            return True, 200, None
        else:
            return notfounderror()
