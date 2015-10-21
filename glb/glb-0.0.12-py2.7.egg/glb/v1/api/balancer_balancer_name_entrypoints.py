# -*- coding: utf-8 -*-
from flask import g

from . import Resource
from glb.core.extensions import db
from glb.core.errors import (notfounderror,
                             badrequesterror)
from glb.models.entrypoint import Entrypoint as EntrypointModel


class BalancerBalancerNameEntrypoints(Resource):

    def get(self, balancer_name):
        result = db.get_entrypoint_list(balancer_name)
        return result, 200, None

    def post(self, balancer_name):
        balancer = db.get_balancer(balancer_name)
        if balancer:
            for e in g.json:
                entrypoint = EntrypointModel.create(**e)
                db.save_or_update_entrypoint(entrypoint, balancer_name)
            db.update_service_latest_version('haproxy')
            return True, 201, None
        else:
            return notfounderror()

    def put(self, balancer_name):
        balancer = db.get_balancer(balancer_name)
        if balancer:
            for e in g.json:
                entrypoint = EntrypointModel.create(**e)
                db.save_or_update_entrypoint(entrypoint, balancer_name)
            db.update_service_latest_version('haproxy')
            return True, 200, None
        else:
            return notfounderror()

    def delete(self, balancer_name):
        domain = g.args.get('domain', '')
        port = g.args.get('port', 0)
        del_type = g.args.get('del_type', 'default')
        if domain and port and del_type == 'default':
            db.delete_entrypoint(balancer_name, domain, port)
            db.update_service_latest_version('haproxy')
            return True, 200, None
        elif del_type == 'all':
            db.delete_all_entrypoint(balancer_name)
            db.update_service_latest_version('haproxy')
            return True, 200, None
        else:
            return badrequesterror()
