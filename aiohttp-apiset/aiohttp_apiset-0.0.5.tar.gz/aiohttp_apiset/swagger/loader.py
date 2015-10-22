

def get_swagger_filepath(self):
    fpath, ipath = self.swagger_ref.split('#')
    if fpath.startswith('/'):
        fpath = fpath[1:]
    else:
        directory = os.path.dirname(sys.modules[self.__module__].__file__)
        fpath = os.path.join(directory, fpath)
    return fpath

def get_swagger(self):
    with open(self.get_swagger_filepath()) as f:
        return yaml.load(f)

@asyncio.coroutine
def swagger(self, request):
    swagger_file = self.get_swagger_filepath()
    return (yield from swagger_yaml(swagger_file)(request))

def add_swagger_route(self, router, prefix=None):
    router.add_route(
        'GET',
        prefix + str(self.version) + self.docs + self.namespace,
        self.swagger,
        name=':'.join((self.namespace, 'swagger')),
        )