from restify import serializers
from restify.resource.base import Resource, ResourceOptions, ResourceMeta


class ModelResourceOptions(ResourceOptions):
    serializer = serializers.ModelSerializer
    model = None
    form_class = None
    queryset = None


class ModelResourceMeta(ResourceMeta):
    options_class = ModelResourceOptions


class ModelResourceMixin(object):
    def get_queryset(self):
        if self._meta.queryset is not None:
            return self.queryset._clone()
        if self._meta.model is not None:
            return self._meta.model._default_manager.all()


class ModelResource(Resource, ModelResourceMixin, metaclass=ModelResourceMeta):
    pass