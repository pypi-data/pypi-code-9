from mc.ioc.dependancy_container import DependencyContainer
from mc.ioc.utils import NoAssertion, IsInstanceOf, HasAttributes, HasMethods

class RequiredFeature(object):

    def __init__(self, feature, assertion=NoAssertion):
        self.feature = feature
        self.assertion = assertion

    def __get__(self, obj, T):
        return self.result # <-- will request the feature upon first call

    def __getattr__(self, name):
        self.result = self.Request()
        return getattr(self.result, name)

    def Request(self):
        obj = DependencyContainer.get_instance()[self.feature]
        assert self.assertion(obj), \
            "The value %r of %r does not match the specified criteria" \
            % (obj, self.feature)
        return obj
