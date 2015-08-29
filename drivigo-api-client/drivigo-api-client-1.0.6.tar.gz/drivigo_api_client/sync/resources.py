# coding: utf-8
from .base import SyncResource


class SyncMarksResource(SyncResource):
    resource_point = ('sync', 'marks')


class SyncModelsResource(SyncResource):
    resource_point = ('sync', 'models')


class SyncBodyTypesResource(SyncResource):
    resource_point = ('sync', 'body_types')


class SyncEnginesResource(SyncResource):
    resource_point = ('sync', 'engines')


class SyncDriveTypesResource(SyncResource):
    resource_point = ('sync', 'drive_types')


class SyncGearBoxTypesResource(SyncResource):
    resource_point = ('sync', 'gear_box_types')


class SyncModelYearResource(SyncResource):
    resource_point = ('sync', 'model_year')


class SyncModificationsResource(SyncResource):
    resource_point = ('sync', 'modifications')


class SyncExchangeTypesResource(SyncResource):
    resource_point = ('sync', 'exchange_types')


class SyncConditionTypesResource(SyncResource):
    resource_point = ('sync', 'condition_types')


class SyncColorsResource(SyncResource):
    resource_point = ('sync', 'colors')


class SyncPaintTypesResource(SyncResource):
    resource_point = ('sync', 'paint_types')


class SyncRudderTypesResource(SyncResource):
    resource_point = ('sync', 'rudder_types')


class SyncPassportTypesResource(SyncResource):
    resource_point = ('sync', 'passport_types')


class SyncCarsResource(SyncResource):
    resource_point = ('sync', 'cars')


class SyncPaymentsResource(SyncResource):
    resource_point = ('sync', 'payments')


class SyncPhotosResource(SyncResource):
    resource_point = ('sync', 'photos')


class SyncDescriptionsResource(SyncResource):
    resource_point = ('sync', 'descriptions')


class SyncContactsResource(SyncResource):
    resource_point = ('sync', 'contacts')


class SyncCarsPublishResource(SyncResource):
    resource_point = ('sync', 'cars', 'publish')

    def get_entrypoint(self, *args, **kwargs):
        nargs = args
        nargs[-2], nargs[-1] = nargs[-1], nargs[-2]
        return super(SyncCarsPublishResource, self).get_entrypoint(*nargs, **kwargs)

class SyncCarsUnpublishResource(SyncResource):
    resource_point = ('sync', 'cars', 'unpublish')

    def get_entrypoint(self, *args, **kwargs):
        nargs = args
        nargs[-2], nargs[-1] = nargs[-1], nargs[-2]
        return super(SyncCarsUnpublishResource, self).get_entrypoint(*nargs, **kwargs)