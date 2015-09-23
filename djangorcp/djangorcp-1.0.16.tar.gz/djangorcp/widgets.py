from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe

from djangorcp.colors import ColorGenerator


class ColorPickerWidget(forms.TextInput):
    class Media:
        css = {
            'all': (
                'djangorcp/colorPicker.css',
            )
        }
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'djangorcp/colorPicker.js',
        )

    def __init__(self, language=None, attrs=None):
        self.language = language or settings.LANGUAGE_CODE[:2]
        super(ColorPickerWidget, self).__init__(attrs=attrs)

    def render_color_list(self, identifier, colors):
        return ''.join([
            '<div class="color-picker" >',
            ''.join(['<span data-field="%s" data-hex="%s" class="color-box" \
                      style="background-color:%s"></span>' %
                     (identifier, c, c) for c in colors]),
            '</div>'
        ])

    def render(self, name, value, attrs=None):
        if 'id' not in attrs:
            attrs['id'] = "id_%s" % name

        parts = []
        generator = ColorGenerator()

        try:
            sat = settings.DJANGORCP['color']['saturation']
            val = settings.DJANGORCP['color']['value']
            colors = generator.get_random_color_set(sat, val)
        except:
            colors = generator.get_random_color_set()

        rendered = super(ColorPickerWidget, self).render(name, value, attrs)
        parts.append(rendered)

        color_list = self.render_color_list(attrs['id'], colors)
        parts.append(color_list)

        return mark_safe(''.join(parts))
