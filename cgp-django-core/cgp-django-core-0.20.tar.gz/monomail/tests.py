from decimal import Decimal
from django.conf import settings
from django.test import TestCase

from .client import MonomailClient

class MonopayTests( TestCase ):
    
    gateway     = None
    cc          = None
    
    test_email  = "kieran@octothorpstudio.com"
    
    def setUp( self ):
        pass

    def test_email(self):
        """Send a Test Email from Template"""
        
        client = MonomailClient()
        client.send_from_template( [ self.test_email ], "Test Email", "email/test-email.html", {} )
        #client.send_from_model( self.test_email )