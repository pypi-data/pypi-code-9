from django import template

register = template.Library()

@register.inclusion_tag('smartmenus/core_css.html')
def smartmenus_core_css(): pass

@register.inclusion_tag('smartmenus/theme_css.html')
def smartmenus_theme_css(theme):
    return {'theme': theme}

@register.inclusion_tag('smartmenus/smartmenus_css.html')
def smartmenus_css(theme):
    return {'theme': theme}

@register.inclusion_tag('smartmenus/core_js.html')
def smartmenus_core_js(): pass

@register.inclusion_tag('smartmenus/init_js.html')
def smartmenus_init_js(): pass

@register.inclusion_tag('smartmenus/smartmenus_js.html')
def smartmenus_js(): pass

@register.inclusion_tag('smartmenus/bootstrap_cms.html', takes_context=True)
def smartmenu_bootstrap_cms(context, theme):
    context['theme'] = theme
    return context
