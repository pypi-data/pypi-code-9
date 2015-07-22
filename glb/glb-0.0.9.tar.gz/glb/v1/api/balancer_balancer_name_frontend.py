# -*- coding: utf-8 -*-
from flask import g

from . import Resource
from glb.models.frontend import Frontend as FrontendModel
from glb.core.extensions import db
from glb.core.errors import notfounderror


class BalancerBalancerNameFrontend(Resource):

    def get(self, balancer_name):
        frontend = db.get_frontend(balancer_name)
        if frontend:
            return frontend, 200, None
        else:
            return notfounderror()

    def put(self, balancer_name):
        res = db.get_frontend(balancer_name)
        if res:
            frontend = g.json
            frontend = FrontendModel(**frontend)
            res = db.update_frontend(frontend, balancer_name)
            print res
            return res, 200, None
        else:
            return notfounderror()
