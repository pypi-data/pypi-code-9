from django.db.models import get_model
from domingo.fields import NonIter, List, AbstractSet


class DjangoFKey(NonIter):

    instance = None
    encoder = staticmethod(int)

    def to_json(self):
        return int(self.value)

    def load(self):
        if not self.instance and self.value and self.django_model:
            Model = get_model(*self.django_model.split('.'))
            self.instance = Model.objects.get(pk=self.value)
        return self.instance


class DjangoFKList(List, AbstractSet):
    index = True

    def __init__(self, *args, **kwargs):
        self.safe_model = kwargs.get('model').replace('.', '__')
        super(DjangoFKList, self).__init__(*args, **kwargs)

    def encoder(self, *args):

        value = super(DjangoFKList, self).encoder(*args)
        for i, v in enumerate(value):
            if not type(v) == dict:
                value[i] = {self.safe_model: v}
        return value

    def prep_query_value(self, value):
        return {self.safe_model: value}

    def get_queryset(self):
        Model = get_model(*self.django_model.split('.'))
        self.queryset = Model.objects.get(
            pk__in=[d.values()[0] for d in self.value]
        )
        return self.queryset
