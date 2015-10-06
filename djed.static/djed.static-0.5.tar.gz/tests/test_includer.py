from pyramid.response import Response
from djed.testing import BaseTestCase


class TestIncluder(BaseTestCase):

    _includes = ('djed.static',)

    def test_components(self):

        def view(request):
            request.include('jquery')
            return Response('<html><head></head><body></body></html>')

        self.config.add_route('view', '/')
        self.config.add_view(view, route_name='view')
        self.config.add_bower_components('tests:static/dir1')

        app = self.make_app()
        response = app.get('/')

        self.assertEqual(response.body, (
            b'<html><head>'
            b'<script type="text/javascript" '
            b'src="/bowerstatic/components/jquery/1.0.0/jquery.js">'
            b'</script></head><body></body></html>'))

        response = app.get('/bowerstatic/components/jquery/1.0.0/jquery.js')

        self.assertEqual(response.body, b'/* dir1/jquery.js */\n')

    def test_components_in_template(self):

        def view(request):
            return {}

        self.config.include('pyramid_chameleon')
        self.config.add_route('view', '/')
        self.config.add_view(
            view, route_name='view', renderer='tests:templates/index.pt')
        self.config.add_bower_components('tests:static/dir1')

        app = self.make_app()
        response = app.get('/')

        self.assertIn(
            b'<script type="text/javascript" '
            b'src="/bowerstatic/components/jquery/1.0.0/jquery.js">'
            b'</script>', response.body)

        response = app.get('/bowerstatic/components/jquery/1.0.0/jquery.js')

        self.assertEqual(response.body, b'/* dir1/jquery.js */\n')

    def test_components_not_exist_errors(self):
        from pyramid.exceptions import ConfigurationError

        self.assertRaises(ConfigurationError, self.request.include, 'jquery')
        self.assertRaises(ConfigurationError, self.request.include, 'not-exist')

    def test_local_component(self):

        def view(request):
            request.include('myapp')
            return Response('<html><head></head><body></body></html>')

        self.config.add_route('view', '/')
        self.config.add_view(view, route_name='view')
        self.config.add_bower_components('tests:static/dir1')
        self.config.add_bower_component('tests:static/local/myapp')

        app = self.make_app()
        response = app.get('/')

        self.assertEqual(response.body, (
            b'<html><head>'
            b'<script type="text/javascript" src='
            b'"/bowerstatic/components/jquery/1.0.0/jquery.js">'
            b'</script>\n<script type="text/javascript" '
            b'src="/bowerstatic/components/myapp/1.0.0/myapp.js"></script>'
            b'</head><body></body></html>'))

        response = app.get('/bowerstatic/components/myapp/1.0.0/myapp.js')

        self.assertEqual(response.body, b'/* myapp.js */\n')

    def test_local_component_in_template(self):

        def view(request):
            return {}

        self.config.include('pyramid_chameleon')
        self.config.add_route('view', '/')
        self.config.add_view(
            view, route_name='view', renderer='tests:templates/index_local.pt')
        self.config.add_bower_components('tests:static/dir1')
        self.config.add_bower_component('tests:static/local/myapp')

        app = self.make_app()
        response = app.get('/')

        self.assertIn((
            b'<script type="text/javascript" src='
            b'"/bowerstatic/components/jquery/1.0.0/jquery.js">'
            b'</script>\n<script type="text/javascript" '
            b'src="/bowerstatic/components/myapp/1.0.0/myapp.js"></script>'),
            response.body)

        response = app.get('/bowerstatic/components/jquery/1.0.0/jquery.js')

        self.assertEqual(response.body, b'/* dir1/jquery.js */\n')

        response = app.get('/bowerstatic/components/myapp/1.0.0/myapp.js')

        self.assertEqual(response.body, b'/* myapp.js */\n')

    def test_custom_components(self):

        def view(request):
            request.include('jquery', 'lib')
            return Response('<html><head></head><body></body></html>')

        self.config.add_route('view', '/')
        self.config.add_view(view, route_name='view')
        self.config.add_bower_components('tests:static/dir1', name='lib')

        app = self.make_app()
        response = app.get('/')

        self.assertEqual(response.body, (
            b'<html><head>'
            b'<script type="text/javascript" '
            b'src="/bowerstatic/lib/jquery/1.0.0/jquery.js">'
            b'</script>'
            b'</head><body></body></html>'))

        response = app.get('/bowerstatic/lib/jquery/1.0.0/jquery.js')

        self.assertEqual(response.body, b'/* dir1/jquery.js */\n')

    def test_custom_local_component(self):

        def view(request):
            request.include('myapp', 'lib')
            return Response('<html><head></head><body></body></html>')

        self.config.add_route('view', '/')
        self.config.add_view(view, route_name='view')
        self.config.add_bower_components('tests:static/dir1', name='lib')
        self.config.add_bower_component('tests:static/local/myapp', 'lib')

        app = self.make_app()
        response = app.get('/')

        self.assertEqual(response.body, (
            b'<html><head>'
            b'<script type="text/javascript" src='
            b'"/bowerstatic/lib/jquery/1.0.0/jquery.js">'
            b'</script>\n<script type="text/javascript" '
            b'src="/bowerstatic/lib/myapp/1.0.0/myapp.js"></script>'
            b'</head><body></body></html>'))

        response = app.get('/bowerstatic/lib/myapp/1.0.0/myapp.js')

        self.assertEqual(response.body, b'/* myapp.js */\n')
