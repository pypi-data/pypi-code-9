from __future__ import absolute_import
from sqlalchemy import create_engine
from pyramda import curry
from .setup_with_session import setup_with_session
from .prepare_models import prepare_models


@curry
def setup_reflective_engine(classname_tablename_dict, connstring):
    engine = create_engine(connstring)
    with_session = setup_with_session(engine)
    models = prepare_models(classname_tablename_dict, engine)
    return models, with_session
