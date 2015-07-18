from .testing import  BaseTestCase
from werkzeug import find_modules

class BaseViewTestCase(BaseTestCase):

    def test_is_view(self):
        self.db._engine.echo = True
        #self.assertEquals(filter(lambda x: not x.startswith('_'),self.db._decl_class_registry.keys()),map(lambda x: find_modules(x),self.app.blueprints.keys()))
        res = self.client.get('/')
        self.assertTrue(True)
