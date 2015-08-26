"""
Tagging components for Django's form library.
"""
from django import forms
from django.shortcuts import resolve_url
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from . import settings
from .models import Tag
import os
from .utils import parse_tag_input


class TagAdminForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name',)

    def clean_name(self):
        value = self.cleaned_data['name']
        tag_names = parse_tag_input(value)
        if len(tag_names) > 1:
            raise forms.ValidationError(_('Multiple tags were given.'))
        elif len(tag_names[0]) > settings.MAX_TAG_LENGTH:
            raise forms.ValidationError(
                _('A tag may be no more than %s characters long.') %
                settings.MAX_TAG_LENGTH)
        return value


class TagField(forms.CharField):
    """
    A ``CharField`` which validates that its input is a valid list of
    tag names.
    """

    def clean(self, value):
        value = super(TagField, self).clean(value)
        if value == '':
            return value
        for tag_name in parse_tag_input(value):
            if len(tag_name) > settings.MAX_TAG_LENGTH:
                raise forms.ValidationError(
                    _('Each tag may be no more than %s characters long.') %
                    settings.MAX_TAG_LENGTH)
        return value


class TagAutocompleteInput(forms.TextInput):
    def _media(self):
        from django.utils import translation
        from django.conf import settings

        lang = translation.get_language().replace('_', '-')
        if lang == 'zh-hans':
            lang = 'zh-CN'
        lang_js = '%slibrary/select2-3.5.2/select2_locale_%s' % (settings.STATIC_URL, lang) if os.path.exists(
            '%slibrary/select2-3.5.2/select2_locale_%s' % (settings.STATIC_ROOT, lang)) else ''
        js = ['%sjavascript/library/select2-3.5.2/select2.js' % settings.STATIC_URL]
        if lang_js:
            js.append(lang_js)

        return forms.Media(css={'all': ['%sjavascript/library/select2-3.5.2/select2.css' % settings.STATIC_URL,
                                        '%sjavascript/library/select2-3.5.2/select2-bootstrap.css' % settings.STATIC_URL]},
                           js=js)

    media = property(_media)

    def render(self, name, value, attrs=None):
        js = u"""<script>
    $(document).ready(function(){{
    $("#{id_for_label}").select2({{
    placeholder: '{placeholder}',
        tags:true,
        multiple: true,
         tokenSeparators: [",", " ",";"],
        ajax: {{
            url: "{url}",
            dataType: 'json',
            data: function (term) {{
                return{{term: term}}
            }},
            results: function (data) {{
                return {{results: data}};
            }}
        }},
        createSearchChoice: function(term, data) {{
            if ($(data).filter(function() {{
              return this.text.localeCompare(term) === 0;
            }}).length === 0) {{
              return {{
                id: term,
                text: term
              }};
            }}
        }},
        initSelection: function (element, callback) {{
            var data = [];
            $(element.val().split(",")).each(function (index,name) {{
                data.push({{id: this, text: name}});
            }});
            callback(data);
        }},
        minimumInputLength: 1,
        triggerChange: true
    }})
    }})
    </script>
    """
        placeholder = ''
        js = js.format(id_for_label=force_text(self.id_for_label('id_%s' % name)),
                       url=force_text(resolve_url('tag_suggestion')), placeholder=placeholder)
        code = u'<input id="{id}" name="{name}" value="{value}" class="form-control select2">'.format(
            id=self.id_for_label('id_%s' % name), name=name, value=value if value else "")
        code = u"%s %s" % (code, js)
        return mark_safe(code)
