# -*- coding: utf-8 -*-
from . import Resource
from glb.core.extensions import db
from glb.core.errors import notfounderror


class NginxName(Resource):

    def get(self, name):
        nginx = db.get_nginx(name)
        if nginx:
            return nginx, 200, None
        else:
            return notfounderror()

    def delete(self, name):
        res = db.delete_nginx(name)
        if res:
            db.update_service_latest_version('nginx')
        return res, 200, None
