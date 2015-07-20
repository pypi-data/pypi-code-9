from json import dumps as parse
import re
from math import ceil
from uuid import uuid4

from django.template import Library, Template
from django.template.loader import get_template, TemplateDoesNotExist

register = Library()

# *****************************************************************************
# ***************************** Libraries *************************************
# *****************************************************************************


# Non JS Component CSS
@register.inclusion_tag('component_css.html')
def component_css():
    return {}


# React libraries
@register.inclusion_tag('react_data.html')
def loadreact():
    return {}


# vanilla javascript
@register.inclusion_tag('vanilla_data.html')
def loadvanilla():
    return {}

# *****************************************************************************
# ************************** Individual Components ****************************
# *****************************************************************************


# Searchable dropdown
@register.inclusion_tag('CustomSearch.html')
def searchable_dropdown(data, name):
    input_id = 'search-{0}'.format(uuid4())
    return {'data': parse(data), 'id': input_id, 'name': name}


# Pagination
@register.inclusion_tag('pagination.html')
def pagination(data, amt, searchable=False):
    el_id = 'pagination-{0}'.format(uuid4())
    return {'data': parse(data), 'perPage': amt,
            'id': el_id, 'searchable': searchable}


# Server-side pagination
@register.inclusion_tag('server-pagination.html')
def server_pagination(data, per_page, page_on):
    page_on = int(page_on) - 1
    pages = int(ceil(float(len(data))/per_page))
    start_point = page_on * per_page
    end_point = start_point + per_page
    print page_on, pages, start_point, end_point
    # modified_data = [data[i] for i in range(start_point, end_point)]
    modified_data = []
    j = 0
    for i in range(start_point, end_point):
        try:
            modified_data.append(data[i])
        except:
            modified_data.append('')
        j = j + 1
    print modified_data
    print page_on
    return {'data': data, 'per_page': per_page, 'endval': pages - 3,
            'pages': pages, 'page_on': page_on, 'rangeset': {
                'pages': range(1, pages), 'begin': range(1, 5),
                'end': range(pages - 3, pages),
                'middle': range(page_on - 1, page_on + 4)},
            'modified_data': modified_data, 'shown_page': page_on + 1}


# Image slider
@register.inclusion_tag('image-slider.html')
def image_slider(imgs):
    el_id = 'image-slider-{0}'.format(uuid4())
    return {'imgs': parse(imgs), 'id': el_id}


# Alerts
@register.inclusion_tag('alert.html', takes_context=True)
def alert(context, alert_type, content, closable=True):
    el_id = 'alert-{0}'.format(uuid4())
    try:
        template = get_template(content)
        rendered_template = template.render(context)
    except TemplateDoesNotExist as tdne:
        template = Template(content)
        if template:
            rendered_template = template.render(context)
        else:
            rendered_template = content
    return {'type': alert_type, 'id': el_id,
            'rendered_template': rendered_template,
            'closable': closable}


# Popover
@register.inclusion_tag('popover.html', takes_context=True)
def popover(context, el_id, content, hover=False, is_template=False):
    popover_id = 'popover-{0}'.format(uuid4())
    try:
        template = get_template(content)
        rendered_template = template.render(context)
        is_template = True
    except TemplateDoesNotExist as tdne:
        template = Template(content)
        r1 = '<[^>]+>'
        r2 = '{%[^>]+%}'
        r3 = '{{[^>]+}}'
        r4 = '{#[^>]+#}'
        if is_template or re.match('{0}|{1}|{2}|{3}'.format(r1, r2, r3, r4), content):
            rendered_template = template.render(context)
            is_template = True
        else:
            rendered_template = content
    return {'content': content, 'hover': hover, 'id': el_id,
            'popover_id': popover_id, 'rendered_template': rendered_template,
            'is_template': is_template}


# Modal
@register.inclusion_tag('modal.html', takes_context=True)
def modal(context, trigger_id, content, closer_id='', is_template=False):
    overlay_id = 'overlay-{0}'.format(uuid4())
    try:
        template = get_template(content)
        rendered_template = template.render(context)
        is_template = True
    except TemplateDoesNotExist as tdne:
        template = Template(content)
        r1 = '<[^>]+>'
        r2 = '{%[^>]+%}'
        r3 = '{{[^>]+}}'
        r4 = '{#[^>]+#}'
        if is_template or re.match('{0}|{1}|{2}|{3}'.format(r1,r2,r3,r4), content):
            rendered_template = template.render(context)
            is_template = True
        else:
            rendered_template = content
    return {'trigger_id': trigger_id, 'overlay_id': overlay_id,
            'rendered_template': rendered_template, 'is_template': is_template,
            'closer_id': closer_id}


# Accordian
@register.inclusion_tag('accordian.html', takes_context=True)
def accordian(context, trigger, content):
    r1 = '<[^>]+>'
    r2 = '{%[^>]+%}'
    r3 = '{{[^>]+}}'
    r4 = '{#[^>]+#}'
    simple_trigger = True
    simple_content = True
    try:
        trigger_template = get_template(trigger)
        rendered_trigger = trigger_template.render(context)
        simple_trigger = False
    except TemplateDoesNotExist as tdne:
        trigger_template = Template(trigger)
        if re.match('{0}|{1}|{2}|{3}'.format(r1, r2, r3, r4), trigger):
            rendered_trigger = trigger_template.render(context)
            simple_trigger = False
        else:
            rendered_trigger = trigger
    try:
        content_template = get_template(content)
        rendered_content = content_template.render(context)
        simple_content = False
    except TemplateDoesNotExist as tdne:
        content_template = Template(content)
        if re.match('{0}|{1}|{2}|{3}'.format(r1, r2, r3, r4), content):
            rendered_content = content_template.render(context)
            simple_content = False
        else:
            rendered_content = content
    return {'trigger': trigger, 'content': content,
            'simple_trigger': simple_trigger, 'simple_content': simple_content,
            'rendered_trigger': rendered_trigger,
            'rendered_content': rendered_content}
