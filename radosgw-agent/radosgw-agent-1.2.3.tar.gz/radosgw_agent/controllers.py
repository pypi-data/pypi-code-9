
class UUIDController(object):

    def __init__(self, uuid):
        self.uuid = uuid

    @expose()
    def index(self):
        if self.uuid:
            items = Foo.objects(id=self.uuid)
            body = ''
            for item in items:
                body += "Foo with UUID " + str(item.id) + "<br>"
            return body
        else:
            abort(404)


class FooController(object):
    @expose(generic=True)
    def index(self):
        return "Foo Controller."

    @index.when(generic=True, method='POST')
    def index_post(self, **kw):
        payload = json.loads(request.body)
        foo = Foo.create(
            id=payload['uuid']
        )
        if foo:
            response.status = 201
        else:
            abort(400)

    @expose()
    def _lookup(self, uuid, *remainder):
        return UUIDController(uuid), remainder


class V1Controller(object):
    foo = FooController()
    bar = BarController()

    @expose()
    def index(self):
        return "Welcome. Take off your jacket and stay awhile."

class RootController(object):
    v1 = V1Controller()

    def __init__(self):
        self.backend = MyBackendSystem()

    @expose(generic=True, template='index.html')
    def index(self):
        return dict()

    @index.when(method='POST')
    def index_post(self, q):
        redirect('http://pecan.readthedocs.org/en/latest/search.html?q=%s' % q)

    @expose('error.html')
    def error(self, status):
        try:
            status = int(status)
        except ValueError:  # pragma: no cover
            status = 500
        message = getattr(status_map.get(status), 'explanation', '')
        return dict(status=status, message=message)
