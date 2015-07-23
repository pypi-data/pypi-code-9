from django.test import TransactionTestCase
from django.core.management import call_command
from django.conf import settings

from cloudantdb.ext.django.loading import cloudantdb_handler
from cloudantdb.exceptions import ResourceError



class CloudantTestCase(TransactionTestCase):  

           
    def _pre_setup(self):
        """Performs any pre-test setup. This includes:

        * If the class has an 'available_apps' attribute, restricting the app
          cache to these applications, then firing post_syncdb -- it must run
          with the correct set of applications for the test case.
        * If the class has a 'fixtures' attribute, installing these fixtures.
        """

        super(CloudantTestCase, self)._pre_setup()
 
        for db_label in settings.CLOUDANTDB_DBS_TEST.keys():
            resp = cloudantdb_handler.get_db(db_label).put().json()
            if resp.has_key('error'):
                raise ResourceError(resp.get('reason'))
        call_command('sync_cloudant',silent=True)
        

    def _post_teardown(self):
        super(CloudantTestCase,self)._post_teardown()
        for db_label in settings.CLOUDANTDB_DBS_TEST.keys():
            resp = cloudantdb_handler.get_db(db_label).delete().json()
            if resp.has_key('error'):
                raise ResourceError(resp.get('reason'))
            
    def _fixture_setup(self):
        super(CloudantTestCase,self)._fixture_setup()
        
    def _fixture_teardown(self):
        super(CloudantTestCase,self)._fixture_teardown()
        
