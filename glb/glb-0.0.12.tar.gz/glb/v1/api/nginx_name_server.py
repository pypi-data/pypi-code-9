# -*- coding: utf-8 -*-
from flask import g

from . import Resource
from glb.core.extensions import db
from glb.core.errors import notfounderror


class NginxNameServer(Resource):

    def get(self, name):
        server = db.get_server(name)
        if server:
            return server, 200, None
        else:
            return notfounderror()

    def put(self, name):
        server = db.get_server(name)
        if server:
            res = db.update_server(g.json, name)
            if res:
                db.update_service_latest_version('nginx')
            return res, 200, None
        else:
            return notfounderror()
