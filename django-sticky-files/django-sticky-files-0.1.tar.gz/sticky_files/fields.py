# coding: utf-8

from django.db.models import ManyToManyField, ForeignKey

from . import widgets as w
from . import conf as c


class StickyFileField(ForeignKey):
    widget_class = w.OneFileWidget

    def __init__(self, to=c.FILE_MODEL, *args, **kwargs):
        super(StickyFileField, self).__init__(to, *args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = self.widget_class
        return super(StickyFileField, self).formfield(**kwargs)


class StickyImageField(StickyFileField):
    widget_class = w.OneImageWidget

    def __init__(self, to=c.IMAGE_MODEL, *args, **kwargs):
        super(StickyImageField, self).__init__(to, *args, **kwargs)


class ManyStickyFileField(ManyToManyField):
    widget_class = w.ManyFileWidget

    def __init__(self, to=c.FILE_MODEL, *args, **kwargs):
        self.max_objects = kwargs.pop('max_objects', None)
        super(ManyStickyFileField, self).__init__(to, *args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = self.widget_class(
            max_objects=self.max_objects,
        )
        return super(ManyStickyFileField, self).formfield(**kwargs)


class ManyStickyImageField(ManyStickyFileField):
    widget_class = w.ManyImageWidget

    def __init__(self, to=c.IMAGE_MODEL, *args, **kwargs):
        super(ManyStickyImageField, self).__init__(to, *args, **kwargs)
