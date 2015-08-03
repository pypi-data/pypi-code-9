import json
from datetime import datetime

from zope import schema
from zope.schema._bootstrapinterfaces import IFromUnicode
from zope.schema.vocabulary import getVocabularyRegistry
from zope.component import getMultiAdapter
from grokcore.component import adapts
from grokcore.component import implementer
from grokcore.component import MultiAdapter

from bst.pygasus.datamanager.interfaces import IModel
from bst.pygasus.datamanager.interfaces import IFieldTransformer


TIME_FORMAT = '%H:%M:%S.%f'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'


class ModelTransfomerUtility(object):
    """ this utility transform a json-request to a
        model. Each model as his named utility.
    """

    def __init__(self, class_, schema):
        self.class_ = class_
        self.schema = schema

    def model(self, request):
        """ return one or more instance of Model
        """
        if request.method == 'GET':
            return [self.class_()]
        return self._readjson(request, self.class_)

    def json(self, models):
        if not isinstance(models, (list, tuple,)):
            return self._json(models)
        else:
            return [self._json(i) for i in models]

    def _json(self, model):
        data = dict()
        for fieldname in self.schema:
            field = self.schema.get(fieldname)
            data[fieldname] = getMultiAdapter((model, field), IFieldTransformer).get()
        return data

    def _readjson(self, request, class_):
        data = json.loads(request.text)['data']

        if not isinstance(data, (list, tuple,)):
            data = [data]

        models = list()
        for row in data:
            model = class_()
            for fieldname in self.schema:
                field = self.schema.get(fieldname)
                if fieldname in row:
                    getMultiAdapter((model, field), IFieldTransformer).set(row[fieldname])
            models.append(model)

        return models


@implementer(IFieldTransformer)
class GenericFieldTransfomer(MultiAdapter):
    adapts(IModel, schema.interfaces.IField)

    def __init__(self, model, field):
        self.model = model
        self.field = field

    def get(self):
        return self.field.get(self.model)

    def set(self, value):
        if value is None:
            self.field.set(self.model, None)
        elif IFromUnicode.providedBy(self.field):
            self.field.set(self.model, self.field.fromUnicode(value))
        else:
            self.field.set(self.model, value)


class DateFieldTransformer(GenericFieldTransfomer):
    adapts(IModel, schema.interfaces.IDate)
    format = DATETIME_FORMAT
    transfomer = lambda s, x: x

    def get(self):
        date = self.field.get(self.model)
        if date is None:
            return date
        return date.strftime(self.format)

    def set(self, value):
        if value is None:
            self.field.set(self.model, None)
        else:
            value = datetime.strptime(value, self.format)
            value = self.transfomer(value)
            self.field.set(self.model, value)


class TimeFieldTransformer(DateFieldTransformer):
    adapts(IModel, schema.interfaces.ITime)
    format = TIME_FORMAT
    transfomer = lambda s, x: x.time()


class IdFieldTransformer(GenericFieldTransfomer):
    adapts(IModel, schema.interfaces.IId)

    def set(self, value):
        if value is None:
            self.field.set(self.model, None)
        else:
            self.field.set(self.model, int(value))


class BoolFieldTransformer(GenericFieldTransfomer):
    adapts(IModel, schema.interfaces.IBool)

    def set(self, value):
        if value is None:
            self.field.set(self.model, None)
        else:
            if not isinstance(value, bool):
                raise TypeError('The value %s is not a boolean' % value)
            self.field.set(self.model, value)


class ChoiceFieldTransformer(GenericFieldTransfomer):
    adapts(IModel, schema.interfaces.IChoice)
    
    def get(self):
        vr = getVocabularyRegistry()
        vocabular = vr.get(None, self.field.vocabularyName)
        return vocabular.getTerm(self.field.get(self.model)).token

    def set(self, value):
        vr = getVocabularyRegistry()
        vocabular = vr.get(None, self.field.vocabularyName)
        term = vocabular.getTermByToken(value)
        if term.value is None:
            self.field.set(self.model, None)
        else:
            self.field.set(self.model, term.value)
