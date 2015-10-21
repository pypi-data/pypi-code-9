# -*- coding: utf-8 -*-
from flask import g

from . import Resource
from glb.core.extensions import db
from glb.core.errors import notfounderror


class NginxNameUpstream(Resource):

    def get(self, name):
        upstream = db.get_upstream(name)
        if upstream:
            return upstream, 200, None
        else:
            return notfounderror()

    def put(self, name):
        res = db.get_upstream(name)
        if res:
            res = db.update_upstream(g.json, name)
            if res:
                db.update_service_latest_version('nginx')
            return res, 200, None
        else:
            return notfounderror()
