import sys
#import mainapp
from notmm.utils.wsgilib import HTTPRequest
from test_support import (
    WSGIControllerTestCase, 
    TestClient, 
    unittest,
    make_app,
    settings,
    ResponseClass
    )

class WSGIAppTestCase(WSGIControllerTestCase):

    def test_render_index(self):
        response = self.client.get('/') # 
        self.assertEqual(response.status_code, '200 OK')

    def test_post_required_with_schevo_db(self):
        req = HTTPRequest()
        req.environ['REQUEST_METHOD'] = 'POST'
        response = self.client.post('/test_post_required_with_schevo_db',
            request=req, data={})
        self.assertEqual(isinstance(response, ResponseClass), True, type(response))
        self.assertEqual(response.status_code, '200 OK')

