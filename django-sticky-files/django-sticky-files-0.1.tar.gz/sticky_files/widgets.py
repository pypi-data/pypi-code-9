# coding: utf-8

from django.forms import Widget
from django.utils.datastructures import MultiValueDict, MergeDict
from django.template.loader import render_to_string
from django.contrib.staticfiles.templatetags.staticfiles import static


class FileWidgetBase(Widget):

    def render(self, name, value, attrs=None):
        ctx = {
            'name': name,
            'value': value,
            'attrs': attrs,
        }
        try:
            ctx.update(self.get_context_data())
        except AttributeError:
            pass
        return render_to_string(self.template, ctx)

    class Media:
        css = {
            'all': [
                static('sticky_files/css/sticky_uploader.css'),
            ]
        }
        js = [
            static('sticky_files/js/sticky_uploader.js'),
        ]


class ManyFileWidget(FileWidgetBase):
    template = 'sticky_files/widgets/many_file_widget.html'

    def __init__(self, max_objects=None, *args, **kwargs):
        self.max_objects = max_objects
        super(ManyFileWidget, self).__init__(*args, **kwargs)

    def value_from_datadict(self, data, files, name):
        if isinstance(data, (MultiValueDict, MergeDict)):
            return data.getlist(name)
        return data.get(name, None)

    def get_context_data(self):
        return {
            'max_objects': self.max_objects,
        }


class ManyImageWidget(FileWidgetBase):
    template = 'sticky_files/widgets/many_image_widget.html'

    def __init__(self, max_objects=None, *args, **kwargs):
        self.max_objects = max_objects
        super(ManyImageWidget, self).__init__(*args, **kwargs)

    def value_from_datadict(self, data, files, name):
        if isinstance(data, (MultiValueDict, MergeDict)):
            return data.getlist(name)
        return data.get(name, None)

    def get_context_data(self):
        return {
            'max_objects': self.max_objects,
        }


class OneFileWidget(FileWidgetBase):
    template = 'sticky_files/widgets/one_file_widget.html'

    def value_from_datadict(self, data, files, name):
        return data.get(name, None)


class OneImageWidget(OneFileWidget):
    template = 'sticky_files/widgets/one_image_widget.html'
