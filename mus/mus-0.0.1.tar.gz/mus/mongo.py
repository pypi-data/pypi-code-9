
import functools

from pymongo import MongoClient
from path import Path


MONGOLIENT = None

def get_client(app):
    global MONGOLIENT
    if MONGOLIENT is None:
        host = app.conf.get('mongohost', 'localhost')
        MONGOCLIENT = MongoClient(host)
    return MONGOCLIENT

def get_channel_db(app):
    client = get_client(app)
    db = client['mus']['channel']
    return(db)

def get_message_db(app):
    client = get_client(app)
    db = client['mus']['mus']
    return(db)
