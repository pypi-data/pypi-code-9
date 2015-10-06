from djed.testing import BaseTestCase


class TestComponents(BaseTestCase):

    _includes = ('djed.static',)

    def test_add(self):

        self.config.add_bower_components('tests:static/dir1')
        self.config.make_wsgi_app()

        bower = self.request.get_bower()

        self.assertIn('components', bower._component_collections)
        self.assertEqual(len(bower._component_collections), 1)

        components = bower._component_collections.get('components')
        self.assertTrue(components.path.endswith('/static/dir1'))

    def test_add_override(self):

        self.config.add_bower_components('tests:static/dir1')
        self.config.commit()
        self.config.add_bower_components('tests:static/dir2')
        self.config.make_wsgi_app()

        bower = self.request.get_bower()
        components = bower._component_collections.get('components')

        self.assertTrue(components.path.endswith('/static/dir2'))

    def test_add_non_existent_dir(self):
        from pyramid.exceptions import ConfigurationError

        self.assertRaises(ConfigurationError, self.config.add_bower_components,
                          'tests:static/not_exists')

    def test_add_conflict_error(self):
        from pyramid.exceptions import ConfigurationConflictError

        self.config.autocommit = False

        self.config.add_bower_components('tests:static/dir1')
        self.config.add_bower_components('tests:static/dir1')

        self.assertRaises(ConfigurationConflictError, self.config.commit)

    def test_add_custom(self):

        self.config.add_bower_components(
            'tests:static/dir1', name='custom')
        self.config.make_wsgi_app()

        bower = self.request.get_bower()

        self.assertIn('custom', bower._component_collections)
        self.assertEqual(len(bower._component_collections), 1)

    def test_add_custom_conflict_error(self):
        from pyramid.exceptions import ConfigurationConflictError

        self.config.autocommit = False

        self.config.add_bower_components('tests:static/dir1', name='custom')
        self.config.add_bower_components('tests:static/dir1', name='custom')

        self.assertRaises(ConfigurationConflictError, self.config.commit)

    def test_add_multiple(self):

        self.config.add_bower_components('tests:static/dir1')
        self.config.add_bower_components('tests:static/dir2', name='custom')
        self.config.make_wsgi_app()

        bower = self.request.get_bower()

        self.assertIn('components', bower._component_collections)
        self.assertIn('custom', bower._component_collections)
