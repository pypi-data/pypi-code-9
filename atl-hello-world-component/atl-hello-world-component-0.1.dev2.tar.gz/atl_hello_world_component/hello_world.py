# encoding=UTF-8
from atl_django_component import Component


class HelloWorld(Component):
    def __init__(self, data_provider="Hello World", version=None):
        super(HelloWorld, self).__init__(data_provider, version)
        self.message = data_provider