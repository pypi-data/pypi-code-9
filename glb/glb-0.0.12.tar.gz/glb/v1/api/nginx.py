# -*- coding: utf-8 -*-
from flask import g

from . import Resource
from glb.core.extensions import db


class Nginx(Resource):

    def get(self):
        nginxs = db.get_nginx_list()
        return nginxs, 200, None

    def post(self):
        nginx_name = g.json['name']
        upstream = g.json['upstream']
        upstream['name'] = nginx_name
        server = g.json['server']
        db.save_nginx(dict(name=nginx_name,
                           upstream=upstream,
                           server=server))
        db.update_service_latest_version('nginx')
        nginx = db.get_nginx(nginx_name)
        return nginx, 201, None
