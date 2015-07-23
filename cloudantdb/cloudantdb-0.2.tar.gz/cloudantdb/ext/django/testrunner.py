from django.conf import settings
from django.test.simple import DjangoTestSuiteRunner
from django.core.management import call_command

from cloudantdb.ext.django.loading import cloudantdb_handler
from cloudantdb.exceptions import ResourceError

class CloudantDBTestSuiteRunner(DjangoTestSuiteRunner):
    """
    A test suite runner for couchdbkit.  This offers the exact same functionality
    as the default django test suite runner, except that it connects all the couchdbkit
    django-extended models to a test database.  The test database is deleted at the
    end of the tests.  To use this, just add this file to your project and the following 
    line to your settings.py file:
    
    TEST_RUNNER = 'myproject.testrunner.CouchDbKitTestSuiteRunner'
    """
    def setup_databases(self, **kwargs):
        for db_label in settings.CLOUDANTDB_DBS.keys():
            print u"Creating test database for label {0}".format(db_label)
            resp = cloudantdb_handler.get_test_db(db_label).put().json()
            if resp.has_key('error'):
                raise ResourceError(resp.get('reason'))
        call_command('sync_cloudant')
        return DjangoTestSuiteRunner.setup_databases(self, **kwargs)
    
    def teardown_databases(self, old_config, **kwargs):
        for db_label in settings.CLOUDANTDB_DBS.keys():
            print u"Deleting test database for label {0}".format(db_label)
            resp = cloudantdb_handler.get_test_db(db_label).delete().json()
            if resp.has_key('error'):
                raise ResourceError(resp.get('reason'))
        DjangoTestSuiteRunner.teardown_databases(self, old_config, **kwargs)