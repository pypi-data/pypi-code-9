import json
import martian

from zope.interface import implementer

from grokcore.component import adapts
from grokcore.component import baseclass
from grokcore.component import MultiAdapter

from webob.exc import HTTPNotFound
from bst.pygasus.datamanager.interfaces import IModel
from bst.pygasus.datamanager.interfaces import IModelHandler


@implementer(IModel)
class ExtBaseModel(object):
    """ Base model for all model used in extjs.
        All model inherit form this class will automatically grokked.

        You will know what a grokker is? So read: https://pypi.python.org/pypi/martian
    """
    martian.baseclass()

    def instance(self):
        """ return new object of same class
        """
        return self.__class__()


@implementer(IModelHandler)
class AbstractModelHandler(MultiAdapter):
    adapts()
    baseclass()

    def __init__(self, model, request):
        self.model = model
        self.request = request
        self.method = dict(GET=self.get,
                           POST=self.create,
                           DELETE=self.delete,
                           PUT=self.update)

    def __call__(self, model, batch):
        return self.method[self.request.method](model, batch)

    def slice(self):
        start = self.request.params.get('start', None)
        limit = self.request.params.get('limit', None)

        if limit is not None and start is not None:
            start = int(start)
            limit = int(limit)
        else:
            limit = None
            start = None

        return start, limit

    def sort(self):
        sort_params = self.request.params.get('sort', None)
        direction = None
        property = None

        if sort_params is not None:
            sort_params = json.loads(sort_params[1:-1])
            direction = sort_params['direction']
            property = sort_params['property']

        return property, direction

    def get(self, model, batch):
        raise NotImplementedError('get method is not implemented')

    def create(self, model, batch):
        raise NotImplementedError('put method is not implemented')

    def delete(self, model, batch):
        raise NotImplementedError('delete method is not implemented')

    def update(self, model, batch):
        raise NotImplementedError('update method is not implemented')
