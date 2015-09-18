__author__ = 'marcos.medeiros'

import locale
from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape
from rapid.views import registry, ModelData
from django.utils.translation import to_locale, get_language

register = template.Library()

try:
    locale.setlocale(locale.LC_ALL, str(to_locale(get_language())))
except:
    locale.setlocale(locale.LC_ALL, str('C'))

def _app_menu(app, request):
    models = list(app.models)
    models.sort(key=lambda m: ModelData(m).model_name(), cmp=locale.strcoll)
    sub = '<li class="menu-group"><div>%s</div><ul class="submenu">\n' % escape(app.menu_name.capitalize())
    has_model = False
    for m in models:
        st = registry.model_entry(m).get('list')
        if st:
            read = st.permission.model(request)
            if read:
                has_model = True
                cd = ModelData(st.model)
                sub += '<li><a href="%s">%s</a></li>\n' % (
                    registry.get_url_of_action(m, 'list'),
                    escape(cd.model_name_plural().title()),
                )
    sub += '</ul></li>\n'
    if has_model:
        return sub
    return ""



@register.simple_tag
def menu(request):
    ret = u"""
    <nav id="menu">
    <style scoped>
        nav li.menu-group{
            cursor: pointer;
        }
        nav li.menu-group.collapsed > ul{
            display: none;
        }
    </style>
    """
    ret += '<ul class="menu">\n'
    mm = registry.modules()
    mm.sort(key=lambda a: a.menu_name, cmp=locale.strcoll)
    for m in mm:
        ret += _app_menu(m, request)
    ret += u"""
    </ul>
    <script>
        $(document).ready(function(){
            $("nav li.menu-group").addClass("collapsed");
            $("nav li.menu-group > div").click(function(){$(this).parent().toggleClass("collapsed")});
        });
    </script>
    </nav>
    """
    return mark_safe(ret)

