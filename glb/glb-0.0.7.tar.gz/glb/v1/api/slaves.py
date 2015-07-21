# -*- coding: utf-8 -*-
from . import Resource
from glb.core.extensions import db


class Slaves(Resource):

    def get(self):
        slaves = db.get_slave_list()
        slaves = [s.as_dict() for s in slaves]
        return slaves, 200, None
