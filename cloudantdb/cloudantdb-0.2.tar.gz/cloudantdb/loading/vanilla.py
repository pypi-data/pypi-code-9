'''
Created on Sep 18, 2014

@author: brian
'''
from .base import CloudantDBHandler
from ..utils import import_util, env

cloudantdb_config = import_util(env('CLOUDANTDB_CONFIG'))
cloudantdb_handler = CloudantDBHandler(cloudantdb_config)

get_db = cloudantdb_handler.get_db