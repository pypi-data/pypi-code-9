# -*- coding: utf-8 -*-
from trytond.pool import Pool
from index import IndexBacklog, DocumentType
from configuration import Configuration


def register():
    "Register models to pool"
    Pool.register(
        Configuration,
        IndexBacklog,
        DocumentType,
        module="elastic_search", type_="model"
    )
