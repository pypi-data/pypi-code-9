from zope import interface


class IModel(interface.Interface):
    """ markerinterface
    """


class IModelHandler(interface.Interface):

    def __call__(self, model):
        """ Handle the model like save it on a database. After
            that return the json result.
        """


class IModelTransformer(interface.Interface):

    def model(self, request):
        """ return a instance of ext.Models with all
            filled json attributes.
        """

    def json(self, model):
        """ return a dict with the data from model. This can
            easily parsed to json.
        """


class IFieldTransformer(interface.Interface):
    """ transform json values to model and model values to json.
    """

    def __init__(self, model, field):
        """ model: instance of IModel
            field: instance of zope.schema.interfaces.IField
        """

    def get(self):
        """ return value from model instance as string
        """

    def set(self, value):
        """ set the value as string as correct type to model instance.
        """


class IJSONExceptionHandler(interface.Interface):
    """ Generic Exception handler for json requests.
    """

    def __call__(self, request):
        """ Handle the exception and write directly to response object.
        """
