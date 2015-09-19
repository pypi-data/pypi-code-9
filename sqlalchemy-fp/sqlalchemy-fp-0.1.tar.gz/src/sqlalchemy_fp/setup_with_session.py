from __future__ import absolute_import
from sqlalchemy.orm import sessionmaker
from .with_session_from import with_session_from


def setup_with_session(engine):
    return with_session_from(sessionmaker(bind=engine))
