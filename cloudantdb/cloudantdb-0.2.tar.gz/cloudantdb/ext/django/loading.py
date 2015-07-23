'''
Created on Sep 17, 2014

@author: brian
'''
import sys

from django.conf import settings

from cloudantdb.loading.base import CloudantDBHandler
if 'test' in sys.argv:
    cloudantdb_handler = CloudantDBHandler(settings.CLOUDANTDB_DBS_TEST)
else:
    cloudantdb_handler = CloudantDBHandler(settings.CLOUDANTDB_DBS)
get_db = cloudantdb_handler.get_db