# -*- coding: utf-8 -*-
from flask import g

from . import Resource
from glb.core.extensions import db
from glb.core.errors import notfounderror
from glb.models.entrypoint import Entrypoint as EntrypointModel


class BalancerBalancerNameEntrypoints(Resource):

    def get(self, balancer_name):
        result = db.get_entrypoint_list(balancer_name)
        return result, 200, None

    def post(self, balancer_name):
        balancer = db.get_balancer(balancer_name)
        if balancer:
            for e in g.json:
                entrypoint = EntrypointModel(**e)
                db.save_entrypoint(entrypoint, balancer_name)
            return True, 201, None
        else:
            return notfounderror()

    def put(self, balancer_name):
        balancer = db.get_balancer(balancer_name)
        if balancer:
            for e in g.json:
                entrypoint = EntrypointModel(**g.json)
                db.save_entrypoint(entrypoint, balancer_name)
            return True, 200, None
        else:
            return notfounderror()

    def delete(self, balancer_name):
        balancer = db.get_balancer(balancer_name)
        if balancer:
            db.delete_entrypoint(balancer_name)
            return True, 200, None
        else:
            return notfounderror()
