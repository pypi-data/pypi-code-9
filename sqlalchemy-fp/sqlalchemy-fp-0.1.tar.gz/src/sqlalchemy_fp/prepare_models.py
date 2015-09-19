from __future__ import absolute_import
from sqlalchemy.ext.declarative import DeferredReflection
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData
from pyramda import curry, map_dict, getattr
from attrdict import AttrDict
from .make_table_class_from import make_table_class_from


@curry
def prepare_models(classname_tablename_dict, engine):
    meta = MetaData()
    Base = automap_base(
        cls=DeferredReflection,
        metadata=meta
    )
    make_table_class = make_table_class_from(Base)
    Base.prepare(engine, reflect=True)

    def get_table_class(attr):
        return getattr(attr, Base.classes)

    models = map_dict(get_table_class, classname_tablename_dict)
    return AttrDict(models)
