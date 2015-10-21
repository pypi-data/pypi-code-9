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
                b = BackendModel.create(**backend)
                db.save_or_update_backend(b, balancer_name)
            db.update_service_latest_version('haproxy')
            return True, 201, None
        else:
            return notfounderror()

    def put(self, balancer_name):
        balancer = db.get_balancer(balancer_name)
        if balancer:
            for backend in g.json:
                b = BackendModel.create(**backend)
                db.save_or_update_backend(b, balancer_name)
            db.update_service_latest_version('haproxy')
            return True, 200, None
        else:
            return notfounderror

    def delete(self, balancer_name):
        address = g.args.get('address', '')
        port = int(g.args.get('port', 0))
        tag = g.args.get('tag', '')
        res = False
        if address and port:
            res = db.delete_backend(balancer_name, address, port)
        if tag:
            res = db.delete_backend_by_tag(balancer_name, tag) or res
        if res:
            db.update_service_latest_version('haproxy')
        return res, 200, None
