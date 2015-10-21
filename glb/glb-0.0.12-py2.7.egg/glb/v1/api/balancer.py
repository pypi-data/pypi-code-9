# -*- coding: utf-8 -*-
from flask import g

from . import Resource
from glb.core.extensions import db
from glb.models.balancer import Balancer as BalancerModel
from glb.models.frontend import Frontend as FrontendModel
from glb.models.entrypoint import Entrypoint as EntrypointModel
from glb.models.backend import Backend as BackendModel


class Balancer(Resource):

    def get(self):
        balancers = db.get_balancer_list()
        return balancers, 200, None

    def post(self):
        data = g.json
        balancer_name = data.get('name')
        frontend = FrontendModel.create(**data.get('frontend'))
        backends = [BackendModel.create(**backend)
                    for backend in data.get('backends', [])]
        entrypoints = [EntrypointModel.create(**entrypoint)
                       for entrypoint in data.get('entrypoints', [])]
        balancer = BalancerModel.create(
            **dict(name=balancer_name,
                   frontend=frontend,
                   backends=backends,
                   entrypoints=entrypoints))
        if db.save_balancer(balancer):
            db.update_service_latest_version('haproxy')
        balancer = db.get_balancer(balancer.name)
        return balancer, 201, None
