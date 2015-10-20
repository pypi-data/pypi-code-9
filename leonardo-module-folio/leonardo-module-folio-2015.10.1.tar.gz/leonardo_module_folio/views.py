# -*- coding: UTF-8 -*-

from django.template.response import SimpleTemplateResponse
from leonardo_module_folio.models import (Category, Client, Project,
                                          ProjectTranslation)


def project_list(request):
    category_list = Category.objects.filter(active=True, parent=None)
    client_list = Client.objects.filter(active=True)
    object_list = Project.objects.filter(active=True)
    context = {
        'object_list': object_list,
        'client_list': client_list,
        'xx': 'xxxxxx',
        'category_list': category_list,
        'in_appcontent_subpage': True
    }
    return SimpleTemplateResponse('folio/project_list.html', context)


def project_detail(request, project_slug=None):
    object = ProjectTranslation.objects.get(slug=project_slug).parent
    return SimpleTemplateResponse(
        'folio/project_detail.html',
        {
            'object': object,
            'in_appcontent_subpage': True
        }
    )
