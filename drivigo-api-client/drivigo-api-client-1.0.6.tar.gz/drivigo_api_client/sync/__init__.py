# coding: utf-8
import copy

import resources



class SyncResources(object):
    __slots__ = ('args', 'kwargs')

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def make_args_kwargs(self, *args, **kwargs):
        kwargs2 = copy.deepcopy(self.kwargs)
        kwargs2.update(kwargs)
        return self.args + args, kwargs2

    def marks(self, *args, **kwargs):
        args2, kwargs2 = self.make_args_kwargs(*args, **kwargs)
        return resources.SyncMarksResource(*args2, **kwargs2)

    def models(self, *args, **kwargs):
        args2, kwargs2 = self.make_args_kwargs(*args, **kwargs)
        return resources.SyncModelsResource(*args2, **kwargs2)

    def body_types(self, *args, **kwargs):
        args2, kwargs2 = self.make_args_kwargs(*args, **kwargs)
        return resources.SyncBodyTypesResource(*args2, **kwargs2)

    def engines(self, *args, **kwargs):
        args2, kwargs2 = self.make_args_kwargs(*args, **kwargs)
        return resources.SyncEnginesResource(*args2, **kwargs2)

    def drive_types(self, *args, **kwargs):
        args2, kwargs2 = self.make_args_kwargs(*args, **kwargs)
        return resources.SyncDriveTypesResource(*args2, **kwargs2)

    def gear_box_types(self, *args, **kwargs):
        args2, kwargs2 = self.make_args_kwargs(*args, **kwargs)
        return resources.SyncGearBoxTypesResource(*args2, **kwargs2)

    def model_year(self, *args, **kwargs):
        args2, kwargs2 = self.make_args_kwargs(*args, **kwargs)
        return resources.SyncModelYearResource(*args2, **kwargs2)

    def modifications(self, *args, **kwargs):
        args2, kwargs2 = self.make_args_kwargs(*args, **kwargs)
        return resources.SyncModificationsResource(*args2, **kwargs2)

    def exchange_types(self, *args, **kwargs):
        args2, kwargs2 = self.make_args_kwargs(*args, **kwargs)
        return resources.SyncExchangeTypesResource(*args2, **kwargs2)

    def condition_types(self, *args, **kwargs):
        args2, kwargs2 = self.make_args_kwargs(*args, **kwargs)
        return resources.SyncConditionTypesResource(*args2, **kwargs2)

    def colors(self, *args, **kwargs):
        args2, kwargs2 = self.make_args_kwargs(*args, **kwargs)
        return resources.SyncColorsResource(*args2, **kwargs2)

    def paint_types(self, *args, **kwargs):
        args2, kwargs2 = self.make_args_kwargs(*args, **kwargs)
        return resources.SyncPaintTypesResource(*args2, **kwargs2)

    def rudder_types(self, *args, **kwargs):
        args2, kwargs2 = self.make_args_kwargs(*args, **kwargs)
        return resources.SyncRudderTypesResource(*args2, **kwargs2)

    def passport_types(self, *args, **kwargs):
        args2, kwargs2 = self.make_args_kwargs(*args, **kwargs)
        return resources.SyncPassportTypesResource(*args2, **kwargs2)

    def cars(self, *args, **kwargs):
        args2, kwargs2 = self.make_args_kwargs(*args, **kwargs)
        return resources.SyncCarsResource(*args2, **kwargs2)

    def cars_publish(self, *args, **kwargs):
        args2, kwargs2 = self.make_args_kwargs(*args, **kwargs)
        return resources.SyncCarsPublishResource(*args2, **kwargs2)

    def cars_unpublish(self, *args, **kwargs):
        args2, kwargs2 = self.make_args_kwargs(*args, **kwargs)
        return resources.SyncCarsUnpublishResource(*args2, **kwargs2)

    def payments(self, *args, **kwargs):
        args2, kwargs2 = self.make_args_kwargs(*args, **kwargs)
        return resources.SyncPaymentsResource(*args2, **kwargs2)

    def photos(self, *args, **kwargs):
        args2, kwargs2 = self.make_args_kwargs(*args, **kwargs)
        return resources.SyncPhotosResource(*args2, **kwargs2)

    def descriptions(self, *args, **kwargs):
        args2, kwargs2 = self.make_args_kwargs(*args, **kwargs)
        return resources.SyncDescriptionsResource(*args2, **kwargs2)

    def contacts(self, *args, **kwargs):
        args2, kwargs2 = self.make_args_kwargs(*args, **kwargs)
        return resources.SyncContactsResource(*args2, **kwargs2)
