#-*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

__all__ = ['get_engine', 'create_session']


def get_engine(host, username, password, database, charset="utf8", encoding="utf-8", pool_recycle=3600):
    return create_engine("mysql+mysqldb://{0}:{1}@{2}/{3}?charset={4}".format(username, password, host, database, charset, encoding), encoding=encoding, pool_recycle=pool_recycle)


def create_session(host, username, password, database, charset="utf8", encoding="utf-8", pool_recycle=3600, autocommit=False, autoflush=False):
    engine = get_engine(host, username, password, database, charset, encoding, pool_recycle)
    return sessionmaker(autocommit=autocommit, autoflush=autoflush, bind=engine)
